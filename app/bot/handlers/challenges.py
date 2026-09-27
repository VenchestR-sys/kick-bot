import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile

from sqlalchemy import select

from app.bot.keyboards.goals import (
    challenge_opponents_keyboard,
    challenge_confirm_keyboard,
    incoming_challenge_keyboard,
    active_challenge_keyboard,
    challenge_progress_keyboard,
    challenge_history_keyboard,
    challenge_menu_keyboard,
    challenge_goals_keyboard,
    challenge_category_keyboard,
)
from app.bot.utils.safe_edit import safe_edit
from app.bot.utils.screens import ScreenManager
from app.locales.texts import t
from app.database.database import async_session
from app.database.models.user import User
from app.database.models.goal import Goal
from app.database.models.challenge import Challenge


router = Router()

challenge_worker_task = None
_bot_instance = None

CHALLENGE_STAKE = 10
CHALLENGE_REWARD = 20

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
CHALLENGES_IMAGE_RU = MEDIA_DIR / "challenges_ru.png"


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def get_user(session, telegram_id: int):
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


def get_challenge_side(challenge: Challenge, user_id: int):
    if challenge.creator_id == user_id:
        return "creator"
    if challenge.opponent_id == user_id:
        return "opponent"
    return None


# =========================================================
# FIND OPPONENT
# =========================================================

@router.callback_query(F.data.startswith("goal:challenge:"))
async def find_opponent_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal).where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(t(lang, "common.goal_not_found"), show_alert=True)
            return

        result = await session.execute(
            select(User).where(User.id != user.id)
        )
        opponents = result.scalars().all()

        if not opponents:
            await safe_edit(
                callback.message,
                f"{t(lang, 'ch.find_opponent')}\n\n"
                f"{t(lang, 'ch.no_players')}",
                reply_markup=challenge_opponents_keyboard([], goal_id, lang),
            )
            await callback.answer()
            return

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.choose_opponent')}\n\n"
            f"🎯 {t(lang, 'ch.goal')}: <b>{goal.title}</b>\n\n"
            f"{t(lang, 'ch.pick_player')}",
            reply_markup=challenge_opponents_keyboard(opponents, goal_id, lang),
        )
        await callback.answer()


# =========================================================
# SELECT OPPONENT
# =========================================================

@router.callback_query(F.data.startswith("challenge:select:"))
async def select_opponent_handler(callback: CallbackQuery):

    parts = callback.data.split(":")
    goal_id = int(parts[2])
    opponent_id = int(parts[3])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal).where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(t(lang, "common.goal_not_found"), show_alert=True)
            return

        result = await session.execute(
            select(User).where(User.id == opponent_id)
        )
        opponent = result.scalar_one_or_none()
        if not opponent:
            await callback.answer(t(lang, "ch.opponent_not_found"), show_alert=True)
            return

        opponent_name = (
            opponent.first_name or opponent.username or t(lang, "common.player")
        )

        if user.balance < CHALLENGE_STAKE:
            await safe_edit(
                callback.message,
                t(
                    lang,
                    "ch.insufficient_kick",
                    stake=CHALLENGE_STAKE,
                    balance=user.balance,
                ),
                reply_markup=challenge_opponents_keyboard(
                    [opponent], goal_id, lang
                ),
            )
            await callback.answer()
            return

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.confirm_title')}\n\n"
            f"🎯 {t(lang, 'ch.goal')}:\n<b>{goal.title}</b>\n\n"
            f"👤 {t(lang, 'ch.opponent')}:\n<b>{opponent_name}</b>\n\n"
            f"🪙 {t(lang, 'ch.stake')}: <b>{CHALLENGE_STAKE} KICK</b>\n"
            f"🏆 {t(lang, 'ch.winner_gets')}: <b>{CHALLENGE_REWARD} KICK</b>\n\n"
            f"{t(lang, 'ch.frozen_notice')}",
            reply_markup=challenge_confirm_keyboard(goal_id, opponent_id, lang),
        )
        await callback.answer()


# =========================================================
# SEND CHALLENGE
# =========================================================

@router.callback_query(F.data.startswith("challenge:send:"))
async def send_challenge_handler(callback: CallbackQuery):

    parts = callback.data.split(":")
    goal_id = int(parts[2])
    opponent_id = int(parts[3])

    async with async_session() as session:

        creator = await get_user(session, callback.from_user.id)
        if not creator:
            await callback.answer()
            return

        lang = creator.language or "ru"

        if creator.balance < CHALLENGE_STAKE:
            await callback.answer(
                t(lang, "ch.insufficient_kick",
                  stake=CHALLENGE_STAKE, balance=creator.balance),
                show_alert=True,
            )
            return

        result = await session.execute(
            select(Goal).where(
                Goal.id == goal_id,
                Goal.user_id == creator.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(t(lang, "common.goal_not_found"), show_alert=True)
            return

        result = await session.execute(
            select(User).where(User.id == opponent_id)
        )
        opponent = result.scalar_one_or_none()
        if not opponent:
            await callback.answer(t(lang, "ch.opponent_not_found"), show_alert=True)
            return

        result = await session.execute(
            select(Challenge).where(
                Challenge.goal_id == goal.id,
                Challenge.creator_id == creator.id,
                Challenge.opponent_id == opponent.id,
                Challenge.status.in_(["pending", "active"]),
            )
        )
        if result.scalar_one_or_none():
            await callback.answer(t(lang, "ch.already_exists"), show_alert=True)
            return

        creator.balance -= CHALLENGE_STAKE
        creator.frozen_kick += CHALLENGE_STAKE

        challenge = Challenge(
            goal_id=goal.id,
            creator_id=creator.id,
            opponent_id=opponent.id,
            category=goal.category,
            duration_days=goal.duration_days,
            kick_stake=CHALLENGE_STAKE,
            creator_progress=0,
            opponent_progress=0,
            creator_score=0,
            opponent_score=0,
            status="pending",
        )
        session.add(challenge)
        await session.flush()

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.sent_title')}\n\n"
            f"🎯 {t(lang, 'ch.goal')}:\n<b>{goal.title}</b>\n\n"
            f"👤 {t(lang, 'ch.opponent')}:\n"
            f"<b>{opponent.first_name or opponent.username or t(lang, 'common.player')}</b>\n\n"
            f"🪙 {t(lang, 'ch.stake')}: <b>{CHALLENGE_STAKE} KICK</b>\n\n"
            f"{t(lang, 'ch.await_accept')}",
        )
        challenge.creator_message_id = callback.message.message_id

        opponent_lang = opponent.language or "ru"

        try:
            opponent_message = await callback.bot.send_message(
                chat_id=opponent.telegram_id,
                text=(
                    f"{t(opponent_lang, 'ch.incoming_title')}\n\n"
                    f"👤 {t(opponent_lang, 'ch.player')}:\n"
                    f"<b>{creator.first_name or creator.username or t(opponent_lang, 'common.player')}</b>\n\n"
                    f"🎯 {t(opponent_lang, 'ch.goal')}:\n<b>{goal.title}</b>\n\n"
                    f"⏱ {t(opponent_lang, 'ch.duration_label')}: "
                    f"<b>{goal.duration_days} {t(opponent_lang, 'common.days')}</b>\n\n"
                    f"🪙 {t(opponent_lang, 'ch.stake')}: "
                    f"<b>{CHALLENGE_STAKE} KICK</b>\n\n"
                    f"{t(opponent_lang, 'ch.accept_hint')}"
                ),
                parse_mode="HTML",
                reply_markup=incoming_challenge_keyboard(challenge.id, opponent_lang),
            )
            challenge.opponent_message_id = opponent_message.message_id

        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(
                f"Could not send challenge to opponent "
                f"{opponent.telegram_id}: {e}"
            )
            challenge.opponent_message_id = None

        await session.commit()
        await callback.answer(
            t(lang, "ch.sent_title").replace("<b>", "").replace("</b>", "")
        )


# =========================================================
# ACCEPT
# =========================================================

@router.callback_query(F.data.startswith("challenge:accept:"))
async def accept_challenge_handler(callback: CallbackQuery):

    challenge_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        opponent = await get_user(session, callback.from_user.id)
        if not opponent:
            await callback.answer()
            return

        lang = opponent.language or "ru"

        result = await session.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            await callback.answer(t(lang, "ch.not_found"), show_alert=True)
            return

        if challenge.opponent_id != opponent.id:
            await callback.answer(t(lang, "ch.not_for_you"), show_alert=True)
            return

        if challenge.status != "pending":
            await callback.answer(t(lang, "ch.already_processed"), show_alert=True)
            return

        if opponent.balance < challenge.kick_stake:
            await callback.answer(
                t(lang, "ch.insufficient_kick",
                  stake=challenge.kick_stake, balance=opponent.balance),
                show_alert=True,
            )
            return

        result = await session.execute(
            select(Goal).where(Goal.id == challenge.goal_id)
        )
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(t(lang, "common.goal_not_found"), show_alert=True)
            return

        result = await session.execute(
            select(User).where(User.id == challenge.creator_id)
        )
        creator = result.scalar_one_or_none()
        if not creator:
            await callback.answer(t(lang, "ch.creator_not_found"), show_alert=True)
            return

        opponent.balance -= challenge.kick_stake
        opponent.frozen_kick += challenge.kick_stake

        challenge.status = "active"
        challenge.start_date = utcnow()
        challenge.deadline = challenge.start_date + timedelta(days=challenge.duration_days)

        await session.commit()

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.accepted_title')}\n\n"
            f"🎯 {t(lang, 'ch.goal')}:\n<b>{goal.title}</b>\n\n"
            f"⏱ {t(lang, 'ch.duration_label')}: "
            f"<b>{challenge.duration_days} {t(lang, 'common.days')}</b>\n\n"
            f"🪙 {t(lang, 'ch.stake')}: <b>{challenge.kick_stake} KICK</b>\n\n"
            f"{t(lang, 'ch.started')}",
            reply_markup=active_challenge_keyboard(challenge.id, lang),
        )
        await callback.answer(t(lang, "ch.started").replace("🔥 ", ""))

        creator_lang = creator.language or "ru"
        try:
            await callback.bot.send_message(
                chat_id=creator.telegram_id,
                text=(
                    f"{t(creator_lang, 'ch.your_accepted')}\n\n"
                    f"🎯 {t(creator_lang, 'ch.goal')}:\n<b>{goal.title}</b>\n\n"
                    f"{t(creator_lang, 'ch.started')}"
                ),
                parse_mode="HTML",
                reply_markup=active_challenge_keyboard(challenge.id, creator_lang),
            )
        except Exception:
            pass


# =========================================================
# DECLINE
# =========================================================

@router.callback_query(F.data.startswith("challenge:decline:"))
async def decline_challenge_handler(callback: CallbackQuery):

    challenge_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            await callback.answer(t(lang, "ch.not_found"), show_alert=True)
            return

        if challenge.opponent_id != user.id:
            await callback.answer(t(lang, "ch.not_yours"), show_alert=True)
            return

        if challenge.status != "pending":
            await callback.answer(t(lang, "ch.already_processed"), show_alert=True)
            return

        result = await session.execute(
            select(User).where(User.id == challenge.creator_id)
        )
        creator = result.scalar_one_or_none()

        if creator:
            creator.balance += challenge.kick_stake
            creator.frozen_kick = max(0, creator.frozen_kick - challenge.kick_stake)

        challenge.status = "declined"
        await session.commit()

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.declined_title')}\n\n"
            f"{t(lang, 'ch.you_declined')}",
        )
        await callback.answer()

        if creator:
            cl = creator.language or "ru"
            try:
                await callback.bot.send_message(
                    chat_id=creator.telegram_id,
                    text=(
                        f"{t(cl, 'ch.declined_title')}\n\n"
                        f"{t(cl, 'ch.opponent_declined_your', stake=challenge.kick_stake)}"
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass


# =========================================================
# VIEW
# =========================================================

@router.callback_query(F.data.startswith("challenge:view:"))
async def view_challenge_handler(callback: CallbackQuery):

    challenge_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            await callback.answer(t(lang, "ch.not_found"), show_alert=True)
            return

        side = get_challenge_side(challenge, user.id)
        if side is None:
            await callback.answer(t(lang, "ch.no_access"), show_alert=True)
            return

        result = await session.execute(select(Goal).where(Goal.id == challenge.goal_id))
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(t(lang, "common.goal_not_found"), show_alert=True)
            return

        result = await session.execute(select(User).where(User.id == challenge.creator_id))
        creator = result.scalar_one_or_none()
        result = await session.execute(select(User).where(User.id == challenge.opponent_id))
        opponent = result.scalar_one_or_none()

        cname = (creator.first_name or creator.username or t(lang, "common.player")) if creator else t(lang, "common.player")
        oname = (opponent.first_name or opponent.username or t(lang, "common.player")) if opponent else t(lang, "common.player")

        my = challenge.creator_progress if side == "creator" else challenge.opponent_progress
        opp = challenge.opponent_progress if side == "creator" else challenge.creator_progress

        if challenge.status == "pending":
            await safe_edit(
                callback.message,
                f"{t(lang, 'ch.pending_title')}\n\n"
                f"🎯 <b>{goal.title}</b>\n\n"
                f"👤 {t(lang, 'ch.creator')}: <b>{cname}</b>\n"
                f"⚔️ {t(lang, 'ch.opponent_short')}: <b>{oname}</b>\n\n"
                f"🪙 {t(lang, 'ch.stake')}: <b>{challenge.kick_stake} KICK</b>\n\n"
                f"{t(lang, 'ch.pending_wait')}",
            )
            await callback.answer()
            return

        if challenge.status in ("completed", "expired", "draw"):
            text = (
                f"{t(lang, 'ch.finished_title')}\n\n"
                f"🎯 <b>{goal.title}</b>\n\n"
                f"👤 {cname}: <b>{challenge.creator_progress}</b>\n"
                f"⚔️ {oname}: <b>{challenge.opponent_progress}</b>\n\n"
            )
            if challenge.status == "draw":
                text += t(lang, "ch.draw")
            elif challenge.winner_id == user.id:
                text += t(lang, "ch.you_win")
            else:
                text += t(lang, "ch.you_lose")

            await safe_edit(callback.message, text)
            await callback.answer()
            return

        remaining = ""
        if challenge.deadline:
            delta = challenge.deadline - utcnow()
            if delta.total_seconds() > 0:
                remaining = (
                    f"\n{t(lang, 'ch.remaining')}: "
                    f"<b>{delta.days} {t(lang, 'common.days')} "
                    f"{delta.seconds // 3600} {t(lang, 'common.hours_short')}</b>\n"
                )
            else:
                remaining = f"\n{t(lang, 'ch.time_up')}\n"

        text = (
            f"{t(lang, 'ch.active_title')}\n\n"
            f"🎯 <b>{goal.title}</b>\n\n"
            f"👤 {cname}: <b>{challenge.creator_progress}</b>\n"
            f"⚔️ {oname}: <b>{challenge.opponent_progress}</b>\n"
            f"{remaining}\n"
            f"🪙 {t(lang, 'ch.bank')}: <b>{challenge.kick_stake * 2} KICK</b>\n"
        )

        if my > opp:
            text += f"\n{t(lang, 'ch.you_ahead')}"
        elif my < opp:
            text += f"\n{t(lang, 'ch.opponent_ahead')}"
        else:
            text += f"\n{t(lang, 'ch.draw_now')}"

        await safe_edit(
            callback.message,
            text,
            reply_markup=challenge_progress_keyboard(challenge.id, lang),
        )
        await callback.answer()


# =========================================================
# COMPLETE TODAY
# =========================================================

@router.callback_query(F.data.startswith("challenge:today:"))
async def challenge_today_handler(callback: CallbackQuery):

    challenge_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            await callback.answer(t(lang, "ch.not_found"), show_alert=True)
            return

        side = get_challenge_side(challenge, user.id)
        if side is None:
            await callback.answer(t(lang, "ch.no_access"), show_alert=True)
            return

        if challenge.status != "active":
            await callback.answer(t(lang, "ch.not_active"), show_alert=True)
            return

        if challenge.deadline and utcnow() >= challenge.deadline:
            await finish_challenge(challenge_id, callback.bot)
            await callback.answer(t(lang, "ch.time_expired"), show_alert=True)
            return

        if challenge.start_date:
            minimum_first_step_time = (
                challenge.start_date + timedelta(hours=1)
            )
            now = utcnow()

            if now < minimum_first_step_time:
                remaining = minimum_first_step_time - now
                total_seconds = int(remaining.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60

                await callback.answer(
                    f"{t(lang, 'ch.first_step_unavailable')} "
                    f"{hours} {t(lang, 'common.hours_short')} "
                    f"{minutes} {t(lang, 'common.minutes_short')}.",
                    show_alert=True,
                )
                return

            days_since = (now - challenge.start_date).days + 1
        else:
            days_since = 1

        current = (
            challenge.creator_progress
            if side == "creator"
            else challenge.opponent_progress
        )

        if current >= days_since:
            await callback.answer(t(lang, "ch.step_already"), show_alert=True)
            return

        if current >= challenge.duration_days:
            await callback.answer(t(lang, "ch.all_steps_done"), show_alert=True)
            return

        if side == "creator":
            challenge.creator_progress += 1
            challenge.creator_score += 5
        else:
            challenge.opponent_progress += 1
            challenge.opponent_score += 5

        await session.commit()

        if (
            challenge.creator_progress >= challenge.duration_days
            and challenge.opponent_progress >= challenge.duration_days
        ):
            await finish_challenge(challenge_id, callback.bot)
            await callback.answer(t(lang, "ch.finished_alert"))
            return

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.pending_title')}\n\n"
            f"{t(lang, 'ch.today_done')}\n\n"
            f"{t(lang, 'ch.your_progress')}: "
            f"<b>{current + 1}/{challenge.duration_days}</b>\n\n"
            f"{t(lang, 'ch.keep_going')}",
            reply_markup=challenge_progress_keyboard(challenge.id, lang),
        )
        await callback.answer(t(lang, "ch.step_done_alert"))


# =========================================================
# FINISH
# =========================================================

async def _send(bot, telegram_id, text):
    if bot is None:
        return
    try:
        await bot.send_message(chat_id=telegram_id, text=text, parse_mode="HTML")
    except Exception:
        pass


async def finish_challenge(challenge_id: int, bot=None):

    bot = bot or _bot_instance

    async with async_session() as session:

        result = await session.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            return
        if challenge.status not in ("active", "pending"):
            return

        result = await session.execute(
            select(User).where(User.id.in_([challenge.creator_id, challenge.opponent_id]))
        )
        users = result.scalars().all()

        creator = next((u for u in users if u.id == challenge.creator_id), None)
        opponent = next((u for u in users if u.id == challenge.opponent_id), None)
        if not creator or not opponent:
            return

        cp = challenge.creator_progress
        op = challenge.opponent_progress

        if cp > op:
            winner, loser = creator, opponent
            challenge.winner_id = creator.id
            challenge.status = "completed"
        elif op > cp:
            winner, loser = opponent, creator
            challenge.winner_id = opponent.id
            challenge.status = "completed"
        else:
            winner = loser = None
            challenge.winner_id = None
            challenge.status = "draw"

        total = challenge.kick_stake * 2

        creator.frozen_kick = max(0, creator.frozen_kick - challenge.kick_stake)
        opponent.frozen_kick = max(0, opponent.frozen_kick - challenge.kick_stake)

        if winner:
            winner.balance += total
        else:
            creator.balance += challenge.kick_stake
            opponent.balance += challenge.kick_stake

        await session.commit()

        cl = creator.language or "ru"
        ol = opponent.language or "ru"

        if winner:
            wp = cp if winner.id == creator.id else op
            wl = winner.language or "ru"
            await _send(bot, winner.telegram_id,
                        t(wl, "ch.win_notification", progress=wp, reward=total))
            await _send(bot, loser.telegram_id,
                        t(loser.language or "ru", "ch.lose_notification"))
        else:
            await _send(bot, creator.telegram_id,
                        t(cl, "ch.draw_notification", stake=challenge.kick_stake))
            await _send(bot, opponent.telegram_id,
                        t(ol, "ch.draw_notification", stake=challenge.kick_stake))


# =========================================================
# HISTORY
# =========================================================

@router.callback_query(F.data == "challenge:history")
async def challenge_history_handler(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Challenge)
            .where((Challenge.creator_id == user.id) | (Challenge.opponent_id == user.id))
            .order_by(Challenge.created_at.desc())
        )
        challenges = result.scalars().all()

        if not challenges:
            text = f"{t(lang, 'ch.history_title')}\n\n{t(lang, 'ch.history_empty')}"
        else:
            text = f"{t(lang, 'ch.history_title')}\n\n"
            for ch in challenges[:20]:
                r = await session.execute(select(Goal).where(Goal.id == ch.goal_id))
                goal = r.scalar_one_or_none()
                gtitle = goal.title if goal else t(lang, "ch.deleted_goal")

                if ch.status == "completed":
                    status = t(lang, "ch.status_win") if ch.winner_id == user.id else t(lang, "ch.status_lose")
                elif ch.status == "draw":
                    status = t(lang, "ch.status_draw")
                elif ch.status == "declined":
                    status = t(lang, "ch.status_declined")
                elif ch.status == "expired":
                    status = t(lang, "ch.status_expired")
                else:
                    status = t(lang, "ch.status_active")

                text += (
                    f"🎯 <b>{gtitle}</b>\n"
                    f"{status}\n"
                    f"📊 {ch.creator_progress} : {ch.opponent_progress}\n\n"
                )

        await safe_edit(
            callback.message,
            text,
            reply_markup=challenge_history_keyboard(lang),
        )
        await callback.answer()


# =========================================================
# MENU
# =========================================================

@router.callback_query(F.data == "challenge:menu")
async def challenge_menu_callback_handler(callback: CallbackQuery):

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        lang = (user.language or "ru") if user else "ru"

    await safe_edit(
        callback.message,
        f"{t(lang, 'ch.title')}\n\n{t(lang, 'ch.subtitle')}",
        reply_markup=challenge_menu_keyboard(lang),
    )
    await callback.answer()


# =========================================================
# CREATE
# =========================================================

@router.callback_query(F.data == "challenge:create")
async def challenge_create_handler(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal).where(
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goals = result.scalars().all()

        if not goals:
            await safe_edit(
                callback.message,
                f"{t(lang, 'ch.create_title')}\n\n"
                f"{t(lang, 'ch.no_active_goals')}",
            )
            await callback.answer()
            return

        await safe_edit(
            callback.message,
            t(lang, "ch.filter_category"),
            reply_markup=challenge_category_keyboard(goals, lang),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("challenge:cat:"))
async def challenge_category_handler(callback: CallbackQuery):

    cat = callback.data.split(":")[2]

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        query = select(Goal).where(
            Goal.user_id == user.id,
            Goal.status == "active",
        )
        if cat != "all":
            query = query.where(Goal.category == cat)

        result = await session.execute(query)
        goals = result.scalars().all()

        if not goals:
            await callback.answer(
                t(lang, "ch.no_active_goals"), show_alert=True,
            )
            return

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.create_title')}\n\n"
            f"{t(lang, 'ch.pick_goal')}",
            reply_markup=challenge_goals_keyboard(goals, lang),
        )

    await callback.answer()


# =========================================================
# SELECT GOAL
# =========================================================

@router.callback_query(F.data.startswith("challenge:goal:"))
async def challenge_goal_select_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal).where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(t(lang, "common.goal_not_found"), show_alert=True)
            return

        result = await session.execute(select(User).where(User.id != user.id))
        opponents = result.scalars().all()

        if not opponents:
            await safe_edit(
                callback.message,
                f"{t(lang, 'ch.choose_opponent')}\n\n{t(lang, 'ch.no_players')}",
                reply_markup=challenge_opponents_keyboard([], goal.id, lang),
            )
            await callback.answer()
            return

        await safe_edit(
            callback.message,
            f"{t(lang, 'ch.pick_opponent_title')}\n\n"
            f"🎯 {t(lang, 'ch.goal')}:\n<b>{goal.title}</b>\n\n"
            f"{t(lang, 'ch.whom')}",
            reply_markup=challenge_opponents_keyboard(opponents, goal.id, lang),
        )
        await callback.answer()


# =========================================================
# MAIN MENU (reply button) — с фото
# =========================================================

@router.message(
    F.text.in_([
        "⚔️ Челленджи",
        "⚔️ Challenges",
        "⚔️ Չելենջներ",
    ])
)
async def challenges_menu_handler(message: Message):

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        text = f"{t(lang, 'ch.title')}\n\n{t(lang, 'ch.subtitle')}"
        markup = challenge_menu_keyboard(lang)

        await ScreenManager.clear_previous(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
        )

        new_message = None

        if CHALLENGES_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                caption = (
                    f"⚔️ <b>CHALLENGES</b>\n\n"
                    f"👇"
                )

            try:
                new_message = await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=FSInputFile(CHALLENGES_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        if new_message is None:
            new_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )

        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await message.delete()


# =========================================================
# WORKER
# =========================================================

async def check_expired_challenges():
    async with async_session() as session:
        result = await session.execute(
            select(Challenge).where(
                Challenge.status == "active",
                Challenge.deadline.isnot(None),
                Challenge.deadline <= utcnow(),
            )
        )
        ids = [c.id for c in result.scalars().all()]

    for cid in ids:
        try:
            await finish_challenge(cid, _bot_instance)
        except Exception:
            pass


async def challenge_expiry_worker():
    while True:
        try:
            await check_expired_challenges()
        except asyncio.CancelledError:
            break
        except Exception:
            pass
        await asyncio.sleep(60)


async def start_challenge_worker(bot):
    global challenge_worker_task, _bot_instance
    _bot_instance = bot
    if challenge_worker_task is not None:
        return
    challenge_worker_task = asyncio.create_task(challenge_expiry_worker())


async def stop_challenge_worker():
    global challenge_worker_task, _bot_instance
    if challenge_worker_task is None:
        return
    challenge_worker_task.cancel()
    try:
        await challenge_worker_task
    except asyncio.CancelledError:
        pass
    challenge_worker_task = None
    _bot_instance = None