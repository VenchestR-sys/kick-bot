import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from aiogram.types import FSInputFile
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.database import async_session
from app.database.models.goal import Goal
from app.database.models.user import User
from app.locales.texts import t
from app.services.goal_calc import calculate_creation_cost


log = logging.getLogger(__name__)

worker_task = None
_bot = None


# =========================================================
# MEDIA
# =========================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "bot" / "media"
GOAL_FAILED_IMAGE_RU = MEDIA_DIR / "goal_failed_ru.png"
GOAL_LOST_IMAGE_RU = MEDIA_DIR / "goal_lost_ru.png"
GOAL_COMPLETED_IMAGE_RU = MEDIA_DIR / "goal_completed_ru.png"


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# =========================================================
# ОТПРАВКА С ФОТО (с фолбэком на текст)
# =========================================================

async def _send_with_photo(telegram_id: int, text: str, image_path: Path | None):
    """Отправляет сообщение с фото и caption. Если фото нет — просто текст."""
    if _bot is None:
        return

    try:
        if image_path is not None and image_path.exists():
            await _bot.send_photo(
                chat_id=telegram_id,
                photo=FSInputFile(image_path),
                caption=text,
                parse_mode="HTML",
            )
        else:
            await _bot.send_message(
                chat_id=telegram_id,
                text=text,
                parse_mode="HTML",
            )
    except Exception:
        log.exception("failed to send notification")


# =========================================================
# ПРОПУСКИ
# =========================================================

async def _check_missed_days():
    """
    Помечает пропущенные шаги.
    - 1 пропуск => предупреждение (фото goal_failed_ru)
    - 2 пропуска подряд => цель failed (фото goal_lost_ru)
    - Дедлайн прошёл => completed (фото goal_completed) или failed
    """
    now = utcnow()

    async with async_session() as session:

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(Goal.status == "active")
        )
        goals = result.scalars().all()

        changed = False

        for goal in goals:

            if not goal.start_date:
                continue

            current_day = (now - goal.start_date).days + 1

            new_missed = 0

            for step in goal.steps:
                if step.status != "pending":
                    continue
                if step.day_number < current_day:
                    step.status = "missed"
                    new_missed += 1
                    changed = True

            if new_missed:
                goal.missed_days_streak = (
                    (goal.missed_days_streak or 0) + new_missed
                )

            # 1 пропуск => предупреждение
            if (
                (goal.missed_days_streak or 0) == 1
                and goal.warning_sent_at is None
                and goal.status == "active"
            ):
                user = await session.get(User, goal.user_id)
                if user:
                    lang = user.language or "ru"
                    text = (
                        f"⚠️ <b>{t(lang, 'reminder.warning_title')}</b>\n\n"
                        f"🎯 <b>{goal.title}</b>\n\n"
                        f"{t(lang, 'reminder.warning_body')}"
                    )
                    await _send_with_photo(
                        user.telegram_id,
                        text,
                        GOAL_FAILED_IMAGE_RU,
                    )
                    goal.warning_sent_at = now

            # 2 пропуска подряд => провал
            if (
                (goal.missed_days_streak or 0) >= 2
                and goal.status == "active"
            ):
                goal.status = "failed"
                changed = True

                user = await session.get(User, goal.user_id)
                if user:
                    cost = calculate_creation_cost(goal.duration_days)
                    user.frozen_kick = max(0, (user.frozen_kick or 0) - cost)

                    lang = user.language or "ru"
                    text = (
                        f"💀 <b>{t(lang, 'goal_failed.title')}</b>\n\n"
                        f"🎯 <b>{goal.title}</b>\n\n"
                        f"{t(lang, 'goal_failed.body')}\n\n"
                        f"🪙 −{cost} KICK"
                    )
                    await _send_with_photo(
                        user.telegram_id,
                        text,
                        GOAL_LOST_IMAGE_RU,
                    )

            # Дедлайн прошёл
            if (
                goal.deadline
                and now > goal.deadline
                and goal.status == "active"
            ):
                all_done = all(
                    s.status == "completed" for s in goal.steps
                )
                goal.status = "completed" if all_done else "failed"
                changed = True

                user = await session.get(User, goal.user_id)
                if user:
                    lang = user.language or "ru"

                    if all_done:
                        text = (
                            f"🏆 <b>{t(lang, 'goals.completed_title')}</b>\n\n"
                            f"🎯 <b>{goal.title}</b>\n\n"
                            f"{t(lang, 'goals.all_steps_done')}"
                        )
                        image = GOAL_COMPLETED_IMAGE_RU
                    else:
                        cost = calculate_creation_cost(goal.duration_days)
                        user.frozen_kick = max(0, (user.frozen_kick or 0) - cost)

                        text = (
                            f"💀 <b>{t(lang, 'goal_failed.title')}</b>\n\n"
                            f"🎯 <b>{goal.title}</b>\n\n"
                            f"{t(lang, 'goal_failed.body')}\n\n"
                            f"🪙 −{cost} KICK"
                        )
                        image = GOAL_LOST_IMAGE_RU

                    await _send_with_photo(user.telegram_id, text, image)

        if changed:
            await session.commit()


# =========================================================
# НАПОМИНАНИЯ
# =========================================================

async def _send_reminders():
    """Отправляет обычные напоминания о невыполненном шаге."""
    if not _bot:
        return

    now = utcnow()
    today = now.date()

    async with async_session() as session:

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(Goal.status == "active")
        )
        goals = result.scalars().all()

        for goal in goals:

            if not goal.start_date:
                continue

            current_day = (now - goal.start_date).days + 1
            current_step = next(
                (s for s in goal.steps if s.day_number == current_day),
                None,
            )

            if not current_step or current_step.status == "completed":
                continue

            if (
                goal.last_reminder_date
                and goal.last_reminder_date.date() == today
            ):
                continue

            user = await session.get(User, goal.user_id)
            if not user or not getattr(user, "goal_notifications", True):
                continue

            lang = user.language or "ru"

            text = (
                f"⏰ <b>{t(lang, 'reminder.regular_title')}</b>\n\n"
                f"🎯 <b>{goal.title}</b>\n\n"
                f"{t(lang, 'reminder.regular_body')}"
            )

            try:
                await _bot.send_message(
                    chat_id=user.telegram_id,
                    text=text,
                    parse_mode="HTML",
                )
                goal.last_reminder_date = now
                await session.commit()
            except Exception:
                log.exception("failed to send reminder")


# =========================================================
# LOOP
# =========================================================

async def _worker_loop():
    while True:
        try:
            await _check_missed_days()
        except asyncio.CancelledError:
            break
        except Exception:
            log.exception("missed_days check failed")

        try:
            await _send_reminders()
        except asyncio.CancelledError:
            break
        except Exception:
            log.exception("reminders failed")

        await asyncio.sleep(3600)


async def start_goal_worker(bot):
    global worker_task, _bot
    _bot = bot
    if worker_task is not None:
        return
    worker_task = asyncio.create_task(_worker_loop())


async def stop_goal_worker():
    global worker_task, _bot
    if worker_task is None:
        return
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass
    worker_task = None
    _bot = None