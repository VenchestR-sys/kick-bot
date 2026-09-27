import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError


logger = logging.getLogger(__name__)


class ChatCleaner:

    @staticmethod
    async def delete_message(
        bot: Bot,
        chat_id: int,
        message_id: int
    ):
        try:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )

            logger.info(
                f"Deleted bot message: {message_id}"
            )

        except TelegramBadRequest as e:
            logger.warning(
                f"Could not delete message {message_id}: {e}"
            )

        except TelegramForbiddenError as e:
            logger.warning(
                f"Telegram forbids deleting message {message_id}: {e}"
            )

    @staticmethod
    async def delete_user_message(message):
        try:
            await message.delete()

            logger.info(
                f"Deleted user message: {message.message_id}"
            )

        except TelegramBadRequest as e:
            logger.warning(
                f"Could not delete user message "
                f"{message.message_id}: {e}"
            )

        except TelegramForbiddenError as e:
            logger.warning(
                f"Telegram forbids deleting user message "
                f"{message.message_id}: {e}"
            )