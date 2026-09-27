from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from sqlalchemy import select

from app.bot.keyboards.main import main_menu
from app.bot.utils.screens import ScreenManager
from app.database.database import async_session
from app.database.models.user import User
from app.services.chat import ChatCleaner

# Активирует автоматическое удержание главного меню
import app.bot.utils.menu  # noqa: F401


router = Router()


# ============================================================
# MEDIA
# ============================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
START_IMAGE_RU = MEDIA_DIR / "start_ru.png"


# ============================================================
# HANDLER
# ============================================================

@router.message(CommandStart())
async def start_handler(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == message.from_user.id
            )
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
            )
            session.add(user)
            await session.flush()

        lang = user.language or "ru"

        text = (
            "⚡ <b>KICK</b>\n\n"
            "Твои цели теперь могут стать игрой.\n\n"
            "🎯 Создавай цели\n"
            "⚔️ Вызывай друзей\n"
            "🔥 Держи streak\n"
            "🏆 Поднимайся в рейтинге\n\n"
            f"🪙 KICK: {user.balance}\n"
            f"⭐ SCORE: {user.score}"
        )

        # --- Удаляем предыдущий экран ---
        await ScreenManager.clear_previous(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
        )

        new_message = None

        # --- Фото, если есть ---
        if START_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                caption = (
                    "⚡ <b>KICK</b>\n\n"
                    "Твои цели теперь могут стать игрой.\n\n"
                    f"🪙 KICK: {user.balance}\n"
                    f"⭐ SCORE: {user.score}"
                )

            try:
                new_message = await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=FSInputFile(START_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=main_menu(lang),
                )
            except Exception:
                new_message = None

        # --- Фолбэк ---
        if new_message is None:
            new_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode="HTML",
                reply_markup=main_menu(lang),
            )

        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await ChatCleaner.delete_user_message(message)