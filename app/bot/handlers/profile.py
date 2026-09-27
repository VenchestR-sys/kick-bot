from pathlib import Path

from aiogram import F, Router
from aiogram.types import (
    Message, CallbackQuery, FSInputFile,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from sqlalchemy import select, func

from app.bot.utils.safe_edit import safe_edit
from app.bot.utils.screens import ScreenManager
from app.constants.achievements import (
    ACHIEVEMENTS, achievement_hint, achievement_name,
)
from app.services.achievements import get_user_achievements
from app.database.database import async_session
from app.database.models.user import User
from app.database.models.goal import Goal
from app.locales.texts import t


router = Router()


# ============================================================
# MEDIA
# ============================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
PROFILE_IMAGE_RU = MEDIA_DIR / "profile_ru.png"


# ============================================================
# HELPERS
# ============================================================

def _ach_button(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=t(lang, "ach.profile_button"),
            callback_data="profile:achievements",
        )
    ]])


async def _build_profile(session, user) -> str:

    lang = user.language or "ru"

    active = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id, Goal.status == "active"
        )
    )).scalar() or 0

    completed = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id, Goal.status == "completed"
        )
    )).scalar() or 0

    cancelled = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id, Goal.status == "cancelled"
        )
    )).scalar() or 0

    failed = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id, Goal.status == "failed"
        )
    )).scalar() or 0

    cur = (user.level - 1) * 100
    nxt = user.level * 100
    in_level = max(0, min(user.xp - cur, nxt - cur))
    req = nxt - cur
    pct = int(in_level / req * 100) if req else 0
    filled = int(pct / 100 * 10)
    bar = "🟩" * filled + "⬜" * (10 - filled)

    return (
        f"{t(lang, 'profile.title')}\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>{user.first_name or user.username or t(lang, 'profile.user')}</b>\n"
        f"🆔 <code>{user.telegram_id}</code>\n\n"
        f"{t(lang, 'profile.balance_title')}\n\n"
        f"{t(lang, 'profile.available')}: <b>{user.balance} KICK</b>\n"
        f"{t(lang, 'profile.in_goals')}: <b>{user.frozen_kick} KICK</b>\n\n"
        f"{t(lang, 'profile.progress_title')}\n\n"
        f"{t(lang, 'profile.level')}: <b>{user.level}</b>\n"
        f"{t(lang, 'profile.xp')}: <b>{user.xp}</b>\n\n"
        f"{bar}\n<code>{in_level}/{req} XP</code>\n\n"
        f"{t(lang, 'profile.score')}: <b>{user.score}</b>\n\n"
        f"{t(lang, 'profile.streak_title')}\n\n"
        f"{t(lang, 'profile.streak_now')}: <b>{user.current_streak} {t(lang, 'profile.days_short')}</b>\n"
        f"{t(lang, 'profile.streak_best')}: <b>{user.best_streak} {t(lang, 'profile.days_short')}</b>\n\n"
        f"{t(lang, 'profile.goals_title')}\n\n"
        f"{t(lang, 'profile.active')}: <b>{active}</b>\n"
        f"{t(lang, 'profile.completed')}: <b>{completed}</b>\n"
        f"{t(lang, 'profile.cancelled')}: <b>{cancelled}</b>\n"
        f"{t(lang, 'goals.status_failed')}: <b>{failed}</b>"
    )


# ============================================================
# PROFILE — с фото для ru
# ============================================================

@router.message(
    F.text.in_(["👤 Профиль", "👤 Profile", "👤 Պրոֆիլ"])
)
async def profile_handler(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return

        lang = user.language or "ru"
        text = await _build_profile(session, user)
        markup = _ach_button(lang)

        # --- Удаляем предыдущий экран ---
        await ScreenManager.clear_previous(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
        )

        new_message = None

        # --- Фото для всех языков ---
        if PROFILE_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                # короткая подпись, если не влезает
                caption = (
                    f"👤 <b>PROFILE</b>\n\n"
                    f"🪙 KICK: <b>{user.balance}</b>\n"
                    f"⭐ SCORE: <b>{user.score}</b>\n"
                    f"🏆 LVL: <b>{user.level}</b>\n\n"
                    f"👇"
                )

            try:
                new_message = await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=FSInputFile(PROFILE_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        # --- Фолбэк, если фото не отправилось ---
        if new_message is None:
            new_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )

        # --- Запоминаем сообщение ---
        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await message.delete()


# ============================================================
# ACHIEVEMENTS
# ============================================================

@router.callback_query(F.data == "profile:achievements")
async def achievements_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return

        lang = user.language or "ru"
        unlocked = await get_user_achievements(session, user.id)

        text = f"{t(lang, 'ach.title')}\n\n"

        for code in ACHIEVEMENTS.keys():
            icon = "✅" if code in unlocked else "🔒"
            text += f"{icon} <b>{achievement_name(code, lang)}</b>\n"
            text += f"   <i>{achievement_hint(code, lang)}</i>\n\n"

        await safe_edit(
            callback.message,
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text=t(lang, "common.back"),
                    callback_data="profile:back",
                )
            ]]),
        )

    await callback.answer()


@router.callback_query(F.data == "profile:back")
async def profile_back_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return

        lang = user.language or "ru"
        text = await _build_profile(session, user)

        await safe_edit(
            callback.message,
            text,
            reply_markup=_ach_button(lang),
        )

    await callback.answer()