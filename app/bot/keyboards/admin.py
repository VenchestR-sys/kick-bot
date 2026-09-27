from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="📊 Статистика", callback_data="admin:stats")
    builder.button(text="👥 Игроки", callback_data="admin:users:0")
    builder.button(text="🔎 Поиск игрока", callback_data="admin:search")
    builder.button(text="🪙 Выдать KICK", callback_data="admin:grant")
    builder.button(text="🚫 Забанить", callback_data="admin:ban")
    builder.button(text="📢 Рассылка", callback_data="admin:broadcast")

    builder.adjust(1)
    return builder.as_markup()


def admin_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="admin:menu",
        )
    ]])


def admin_users_keyboard(users, page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for u in users:
        name = u.first_name or u.username or f"id{u.telegram_id}"
        builder.button(
            text=f"👤 {name}",
            callback_data=f"admin:user:{u.id}",
        )

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=f"admin:users:{page - 1}",
        ))
    nav.append(InlineKeyboardButton(
        text=f"{page + 1}/{total_pages}",
        callback_data="admin:noop",
    ))
    if page + 1 < total_pages:
        nav.append(InlineKeyboardButton(
            text="➡️",
            callback_data=f"admin:users:{page + 1}",
        ))

    builder.adjust(1)
    markup = builder.as_markup()
    markup.inline_keyboard.append(nav)
    markup.inline_keyboard.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="admin:menu",
    )])
    return markup


def admin_user_keyboard(user_id: int, is_banned: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🪙 +50 KICK", callback_data=f"admin:addkick:{user_id}:50")
    builder.button(text="🪙 +100 KICK", callback_data=f"admin:addkick:{user_id}:100")
    builder.button(text="💸 −50 KICK", callback_data=f"admin:subkick:{user_id}:50")
    builder.button(
        text=("✅ Разбанить" if is_banned else "🚫 Забанить"),
        callback_data=f"admin:toggleban:{user_id}",
    )
    builder.button(text="🔙 К игрокам", callback_data="admin:users:0")

    builder.adjust(2, 1, 1, 1)
    return builder.as_markup()