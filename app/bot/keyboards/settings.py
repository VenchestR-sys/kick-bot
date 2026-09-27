from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.locales.texts import t


def settings_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t(language, "settings.notifications"),
                callback_data="settings:notifications"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.language"),
                callback_data="settings:language"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.data"),
                callback_data="settings:data"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.main_menu"),
                callback_data="settings:main_menu"
            )],
        ]
    )


def language_keyboard(language: str) -> InlineKeyboardMarkup:
    ru_s = " ✅" if language == "ru" else ""
    en_s = " ✅" if language == "en" else ""
    hy_s = " ✅" if language == "hy" else ""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🇷🇺 Русский{ru_s}", callback_data="language:ru")],
            [InlineKeyboardButton(text=f"🇬🇧 English{en_s}", callback_data="language:en")],
            [InlineKeyboardButton(text=f"🇦🇲 Հայերեն{hy_s}", callback_data="language:hy")],
            [InlineKeyboardButton(
                text=t(language, "settings.back"),
                callback_data="settings:back"
            )],
        ]
    )


def notifications_keyboard(language, goal_notifications, challenge_notifications, achievement_notifications):
    g = "✅" if goal_notifications else "❌"
    c = "✅" if challenge_notifications else "❌"
    a = "✅" if achievement_notifications else "❌"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{t(language, 'settings.goal_notifications')}: {g}",
                callback_data="settings:toggle_goal_notifications"
            )],
            [InlineKeyboardButton(
                text=f"{t(language, 'settings.challenge_notifications')}: {c}",
                callback_data="settings:toggle_challenge_notifications"
            )],
            [InlineKeyboardButton(
                text=f"{t(language, 'settings.achievement_notifications')}: {a}",
                callback_data="settings:toggle_achievement_notifications"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.back"),
                callback_data="settings:back"
            )],
        ]
    )


def data_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t(language, "settings.delete_goals"),
                callback_data="data:delete_goals"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.reset_progress"),
                callback_data="data:reset_progress"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.delete_account"),
                callback_data="data:delete_account"
            )],
            [InlineKeyboardButton(
                text=t(language, "settings.back"),
                callback_data="settings:back"
            )],
        ]
    )


def confirm_delete_account_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(language, "settings.cancel"),
                    callback_data="data:cancel"
                ),
                InlineKeyboardButton(
                    text=t(language, "settings.confirm_delete"),
                    callback_data="data:confirm_delete_account"
                ),
            ]
        ]
    )


def confirm_delete_goals_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(language, "settings.cancel"),
                    callback_data="data:cancel"
                ),
                InlineKeyboardButton(
                    text=t(language, "settings.confirm_delete_goals"),
                    callback_data="data:confirm_delete_goals"
                ),
            ]
        ]
    )


def confirm_reset_progress_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(language, "settings.cancel"),
                    callback_data="data:cancel"
                ),
                InlineKeyboardButton(
                    text=t(language, "settings.confirm_reset_progress"),
                    callback_data="data:confirm_reset_progress"
                ),
            ]
        ]
    )