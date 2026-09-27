from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.locales.texts import t


def main_menu(language: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(language, "menu.my_goals")),
                KeyboardButton(text=t(language, "menu.profile")),
            ],
            [
                KeyboardButton(text=t(language, "menu.rating")),
                KeyboardButton(text=t(language, "menu.challenges")),
            ],
            [
                KeyboardButton(text=t(language, "menu.bonus")),
                KeyboardButton(text=t(language, "menu.settings")),
            ],
            [
                KeyboardButton(text=t(language, "menu.help")),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True,
    )