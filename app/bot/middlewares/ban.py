# app/bot/middlewares/ban.py
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from app.database.database import async_session
from app.database.models.user import User


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id is not None:
            async with async_session() as session:
                result = await session.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = result.scalar_one_or_none()
                if user and getattr(user, "is_banned", False):
                    if isinstance(event, CallbackQuery):
                        await event.answer(
                            "🚫 Вы забанены.", show_alert=True,
                        )
                    return
        return await handler(event, data)