from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.bot.utils.screens import ScreenManager
from app.database.database import async_session
from app.database.models.user import User
from app.locales.texts import t


router = Router()


# ============================================================
# MEDIA
# ============================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
HELP_IMAGE_RU = MEDIA_DIR / "help_ru.png"


# ============================================================
# HELPERS
# ============================================================

SUPPORTED = ("ru", "en", "hy")


def _pick_language(user: User | None, tg_lang: str | None) -> str:
    if user and user.language in SUPPORTED:
        return user.language
    if tg_lang and tg_lang[:2] in SUPPORTED:
        return tg_lang[:2]
    return "ru"


async def _get_user(session, telegram_id: int):
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def _show_help(bot, chat_id: int, telegram_id: int, tg_lang: str | None):

    async with async_session() as session:

        user = await _get_user(session, telegram_id)
        if not user:
            return

        lang = _pick_language(user, tg_lang)

        text = (
            f"{t(lang, 'help.title')}\n\n"
            f"{t(lang, 'help.body')}\n\n"
            f"{t(lang, 'help.commands')}"
        )

        # --- Удаляем предыдущий экран ---
        await ScreenManager.clear_previous(
            bot=bot,
            user=user,
            chat_id=chat_id,
            session=session,
        )

        new_message = None

        # --- Фото для всех языков ---
        if HELP_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                # короткая подпись, если не влезает
                caption = (
                    f"{t(lang, 'help.title')}\n\n"
                    f"📚 {t(lang, 'help.commands').split(chr(10))[0]}\n\n"
                    f"👇"
                )

            try:
                new_message = await bot.send_photo(
                    chat_id=chat_id,
                    photo=FSInputFile(HELP_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                )
            except Exception:
                new_message = None

        # --- Фолбэк ---
        if new_message is None:
            new_message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML",
            )

        # --- Запоминаем сообщение ---
        user.last_bot_message_id = new_message.message_id
        await session.commit()


# ============================================================
# HANDLERS
# ============================================================

@router.message(Command("help"))
async def cmd_help(message: Message):
    await _show_help(
        message.bot,
        message.chat.id,
        message.from_user.id,
        message.from_user.language_code,
    )
    await message.delete()


@router.message(
    F.text.in_([
        "❓ Помощь",
        "❓ Help",
        "❓ Օգնություն",
    ])
)
async def btn_help(message: Message):
    await _show_help(
        message.bot,
        message.chat.id,
        message.from_user.id,
        message.from_user.language_code,
    )
    await message.delete()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):

    await state.clear()

    async with async_session() as session:

        user = await _get_user(session, message.from_user.id)
        if not user:
            return

        lang = _pick_language(user, message.from_user.language_code)

        await ScreenManager.show(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
            text=t(lang, "help.cancelled"),
        )

    await message.delete()