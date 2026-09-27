from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.locales.texts import t


def rating_keyboard(language: str = "ru", current_type: str = "score") -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    score_text = f"🏆 {t(language, 'rating.metric_score')}" if current_type == "score" else f"⭐ {t(language, 'rating.metric_score')}"
    streak_text = f"🔥 {t(language, 'rating.metric_streak')}"
    xp_text = f"⚡ {t(language, 'rating.metric_xp')}"

    builder.button(text=score_text, callback_data="rating:score")
    builder.button(text=streak_text, callback_data="rating:streak")
    builder.button(text=xp_text, callback_data="rating:xp")

    builder.adjust(3)
    return builder.as_markup()