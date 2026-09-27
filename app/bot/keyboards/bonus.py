from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.locales.texts import t


def bonus_menu_keyboard(language: str = "ru", user=None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # 1. Канал
    if user and getattr(user, "bonus_channel_claimed", False):
        channel_text = f"✅ {t(language, 'bonus.channel_title').replace('<b>','').replace('</b>','')}"
    else:
        channel_text = f"📢 {t(language, 'bonus.channel_title').replace('<b>','').replace('</b>','')}"

    builder.button(text=channel_text, callback_data="bonus:channel")

    # 2. 3 дня
    builder.button(
        text=f"🔥 {t(language, 'bonus.streak3_title').replace('<b>','').replace('</b>','')}",
        callback_data="bonus:streak3",
    )

    # 3. 5 дней
    builder.button(
        text=f"⚡ {t(language, 'bonus.streak5_title').replace('<b>','').replace('</b>','')}",
        callback_data="bonus:streak5",
    )

    builder.adjust(1)
    return builder.as_markup()


def bonus_channel_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "bonus.channel_button_go"),
        url="https://t.me/kickgame_official",
    )
    builder.button(
        text=t(language, "bonus.channel_button"),
        callback_data="bonus:channel:check",
    )
    builder.button(
        text=t(language, "bonus.back"),
        callback_data="bonus:menu",
    )

    builder.adjust(1)
    return builder.as_markup()


def bonus_streak_keyboard(language: str = "ru", which: str = "3") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "bonus.claim_button"),
        callback_data=f"bonus:streak{which}:claim",
    )
    builder.button(
        text=t(language, "bonus.back"),
        callback_data="bonus:menu",
    )

    builder.adjust(1)
    return builder.as_markup()