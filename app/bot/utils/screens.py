from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.services.chat import ChatCleaner


class ScreenManager:

    @staticmethod
    async def clear_previous(
        bot: Bot,
        user: User,
        chat_id: int,
        session: AsyncSession
    ):
        if user.last_bot_message_id:

            await ChatCleaner.delete_message(
                bot=bot,
                chat_id=chat_id,
                message_id=user.last_bot_message_id
            )

            user.last_bot_message_id = None

            await session.commit()

    @staticmethod
    async def show(
        bot: Bot,
        user: User,
        chat_id: int,
        session: AsyncSession,
        text: str,
        reply_markup=None
    ) -> Message:

        await ScreenManager.clear_previous(
            bot=bot,
            user=user,
            chat_id=chat_id,
            session=session
        )

        new_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

        user.last_bot_message_id = new_message.message_id

        await session.commit()

        return new_message