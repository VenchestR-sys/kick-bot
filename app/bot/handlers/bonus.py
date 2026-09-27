from datetime import datetime, timedelta, timezone
from pathlib import Path

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from sqlalchemy import select

from app.bot.keyboards.bonus import (
    bonus_menu_keyboard,
    bonus_channel_keyboard,
    bonus_streak_keyboard,
)
from app.bot.utils.safe_edit import safe_edit
from app.bot.utils.screens import ScreenManager
from app.database.database import async_session
from app.database.models.user import User
from app.locales.texts import t


router = Router()


# ============================================================
# MEDIA
# ============================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
BONUS_IMAGE_RU = MEDIA_DIR / "bonus_ru.png"


CHANNEL_ID = "@kickgame_official"
CHANNEL_BONUS = 50
STREAK3_BONUS = 10
STREAK5_BONUS = 30


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _can_claim_again(last_claim: datetime | None) -> bool:
    """Раз в 7 дней."""
    if last_claim is None:
        return True
    return utcnow() - last_claim >= timedelta(days=7)


async def get_user(session, telegram_id: int):
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


# =========================================================
# REPLY-КНОПКА «🎁 Бонус»
# =========================================================

@router.message(
    F.text.in_([
        "🎁 Бонус",
        "🎁 Bonus",
        "🎁 Բոնուս",
    ])
)
async def bonus_menu_handler(message: Message):

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        text = (
            f"{t(lang, 'bonus.title')}\n\n"
            f"{t(lang, 'bonus.subtitle')}"
        )
        markup = bonus_menu_keyboard(lang, user)

        # Удаляем предыдущий экран
        await ScreenManager.clear_previous(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
        )

        new_message = None

        # Фото для всех языков
        if BONUS_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                caption = (
                    f"{t(lang, 'bonus.title')}\n\n"
                    f"👇"
                )

            try:
                new_message = await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=FSInputFile(BONUS_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        # Фолбэк
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
# ВОЗВРАТ К МЕНЮ
# =========================================================

@router.callback_query(F.data == "bonus:menu")
async def bonus_menu_callback(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            f"{t(lang, 'bonus.title')}\n\n{t(lang, 'bonus.subtitle')}",
            reply_markup=bonus_menu_keyboard(lang, user),
        )

    await callback.answer()


# =========================================================
# ЗАДАНИЕ 1: ПОДПИСКА НА КАНАЛ
# =========================================================

@router.callback_query(F.data == "bonus:channel")
async def bonus_channel_callback(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        if getattr(user, "bonus_channel_claimed", False):
            await safe_edit(
                callback.message,
                f"{t(lang, 'bonus.channel_title')}\n\n"
                f"{t(lang, 'bonus.channel_claimed')}",
                reply_markup=bonus_channel_keyboard(lang),
            )
            await callback.answer()
            return

        await safe_edit(
            callback.message,
            f"{t(lang, 'bonus.channel_title')}\n\n"
            f"{t(lang, 'bonus.channel_body')}",
            reply_markup=bonus_channel_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "bonus:channel:check")
async def bonus_channel_check(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        if getattr(user, "bonus_channel_claimed", False):
            await callback.answer(
                t(lang, "bonus.channel_claimed").replace("<b>", "").replace("</b>", ""),
                show_alert=True,
            )
            return

        # Проверяем подписку через Bot API
        try:
            member = await callback.bot.get_chat_member(
                chat_id=CHANNEL_ID,
                user_id=callback.from_user.id,
            )
            is_subscribed = member.status in ("member", "administrator", "creator")
        except Exception:
            await callback.answer(
                t(lang, "bonus.channel_check_error"),
                show_alert=True,
            )
            return

        if not is_subscribed:
            await callback.answer(
                t(lang, "bonus.channel_not_subscribed"),
                show_alert=True,
            )
            return

        # Начисляем
        user.bonus_channel_claimed = True
        user.balance += CHANNEL_BONUS
        await session.commit()

        await safe_edit(
            callback.message,
            f"{t(lang, 'bonus.channel_title')}\n\n"
            f"{t(lang, 'bonus.channel_success')}",
            reply_markup=bonus_channel_keyboard(lang),
        )

    await callback.answer()


# =========================================================
# ЗАДАНИЕ 2: 3 ДНЯ ПОДРЯД
# =========================================================

@router.callback_query(F.data == "bonus:streak3")
async def bonus_streak3_callback(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            f"{t(lang, 'bonus.streak3_title')}\n\n"
            f"{t(lang, 'bonus.streak3_body')}\n\n"
            f"🔥 Streak: <b>{user.current_streak}</b>",
            reply_markup=bonus_streak_keyboard(lang, "3"),
        )

    await callback.answer()


@router.callback_query(F.data == "bonus:streak3:claim")
async def bonus_streak3_claim(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        # Проверка streak
        if user.current_streak < 3:
            await callback.answer(
                t(lang, "bonus.not_enough_streak", streak=user.current_streak),
                show_alert=True,
            )
            return

        # Раз в неделю
        if not _can_claim_again(user.bonus_streak3_last_claim):
            await callback.answer(
                t(lang, "bonus.week_wait"),
                show_alert=True,
            )
            return

        user.balance += STREAK3_BONUS
        user.bonus_streak3_last_claim = utcnow()
        await session.commit()

        await safe_edit(
            callback.message,
            t(lang, "bonus.claim_success", amount=STREAK3_BONUS),
            reply_markup=bonus_streak_keyboard(lang, "3"),
        )

    await callback.answer()


# =========================================================
# ЗАДАНИЕ 3: 5 ДНЕЙ ПОДРЯД
# =========================================================

@router.callback_query(F.data == "bonus:streak5")
async def bonus_streak5_callback(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            f"{t(lang, 'bonus.streak5_title')}\n\n"
            f"{t(lang, 'bonus.streak5_body')}\n\n"
            f"🔥 Streak: <b>{user.current_streak}</b>",
            reply_markup=bonus_streak_keyboard(lang, "5"),
        )

    await callback.answer()


@router.callback_query(F.data == "bonus:streak5:claim")
async def bonus_streak5_claim(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        if user.current_streak < 5:
            await callback.answer(
                t(lang, "bonus.not_enough_streak", streak=user.current_streak),
                show_alert=True,
            )
            return

        if not _can_claim_again(user.bonus_streak5_last_claim):
            await callback.answer(
                t(lang, "bonus.week_wait"),
                show_alert=True,
            )
            return

        user.balance += STREAK5_BONUS
        user.bonus_streak5_last_claim = utcnow()
        await session.commit()

        await safe_edit(
            callback.message,
            t(lang, "bonus.claim_success", amount=STREAK5_BONUS),
            reply_markup=bonus_streak_keyboard(lang, "5"),
        )

    await callback.answer()