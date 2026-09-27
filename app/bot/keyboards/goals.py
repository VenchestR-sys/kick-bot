from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.constants.categories import CATEGORIES
from app.locales.texts import t


# =========================================================
# СОЗДАНИЕ ЦЕЛИ
# =========================================================

def duration_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=t(language, "btn.duration.1"), callback_data="duration:1")
    builder.button(text=t(language, "btn.duration.3"), callback_data="duration:3")
    builder.button(text=t(language, "btn.duration.7"), callback_data="duration:7")
    builder.button(text=t(language, "btn.duration.14"), callback_data="duration:14")
    builder.button(text=t(language, "btn.duration.30"), callback_data="duration:30")
    builder.button(text=t(language, "btn.duration.90"), callback_data="duration:90")
    builder.button(text=t(language, "btn.duration.custom"), callback_data="duration:custom")

    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()


def goal_preview_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=t(language, "btn.start"), callback_data="goal:start")
    builder.button(text=t(language, "btn.edit"), callback_data="goal:edit")
    builder.button(text=t(language, "btn.cancel"), callback_data="goal:cancel")

    builder.adjust(1)
    return builder.as_markup()


def goal_edit_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=t(language, "btn.edit_title"), callback_data="goal:edit:title")
    builder.button(text=t(language, "btn.edit_category"), callback_data="goal:edit:category")
    builder.button(text=t(language, "btn.edit_description"), callback_data="goal:edit:description")
    builder.button(text=t(language, "btn.edit_result"), callback_data="goal:edit:result")
    builder.button(text=t(language, "btn.edit_duration"), callback_data="goal:edit:duration")
    builder.button(text=t(language, "btn.back"), callback_data="goal:edit:back")

    builder.adjust(1)
    return builder.as_markup()


# =========================================================
# КАТЕГОРИИ
# =========================================================

def category_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for code, cat in CATEGORIES.items():
        builder.button(
            text=f"{cat['emoji']} {cat.get(language) or cat['ru']}",
            callback_data=f"goal:category:{code}",
        )

    builder.adjust(2)
    return builder.as_markup()


def description_step_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t(language, "btn.skip"),
        callback_data="goal:desc:skip",
    )
    builder.adjust(1)
    return builder.as_markup()


def result_step_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t(language, "btn.skip"),
        callback_data="goal:result:skip",
    )
    builder.adjust(1)
    return builder.as_markup()


def note_skip_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t(language, "btn.skip"),
        callback_data="goal:today:skip_note",
    )
    builder.adjust(1)
    return builder.as_markup()


# =========================================================
# СПИСОК ЦЕЛЕЙ
# =========================================================

def goals_list_keyboard(goals, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for goal in goals:
        title = goal.title
        if len(title) > 30:
            title = title[:30] + "..."

        builder.button(
            text=f"🎯 {title}",
            callback_data=f"goal:view:{goal.id}",
        )

    builder.button(text=t(language, "btn.create_goal"), callback_data="goal:create")
    builder.adjust(1)
    return builder.as_markup()


def create_goal_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(language, "btn.create_goal"), callback_data="goal:create")
    return builder.as_markup()


# =========================================================
# КАРТОЧКА ЦЕЛИ
# =========================================================

def goal_detail_keyboard(
    goal_id: int,
    can_cancel: bool = True,
    language: str = "ru",
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "btn.find_opponent"),
        callback_data=f"goal:challenge:{goal_id}",
    )
    builder.button(
        text=t(language, "btn.complete_today"),
        callback_data=f"goal:today:{goal_id}",
    )
    builder.button(
        text=t(language, "btn.heatmap"),
        callback_data=f"goal:heatmap:{goal_id}",
    )
    builder.button(
        text=t(language, "btn.all_steps"),
        callback_data=f"goal:steps:{goal_id}",
    )

    if can_cancel:
        builder.button(
            text=t(language, "btn.cancel_goal"),
            callback_data=f"goal:cancel_goal:{goal_id}",
        )

    builder.button(text=t(language, "btn.back"), callback_data="goal:list")

    builder.adjust(1)
    return builder.as_markup()


def steps_keyboard(goal_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "btn.back_to_goal"),
        callback_data=f"goal:view:{goal_id}",
    )
    builder.button(
        text=t(language, "btn.back_to_goals"),
        callback_data="goal:list",
    )

    builder.adjust(1)
    return builder.as_markup()


def cancel_goal_keyboard(goal_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "btn.yes_cancel"),
        callback_data=f"goal:confirm_cancel:{goal_id}",
    )
    builder.button(
        text=t(language, "btn.no_back"),
        callback_data=f"goal:cancel_back:{goal_id}",
    )

    builder.adjust(1)
    return builder.as_markup()


# =========================================================
# ЧЕЛЛЕНДЖИ
# =========================================================

def challenge_confirm_keyboard(
    goal_id: int, opponent_id: int, language: str = "ru",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "btn.throw_challenge"),
        callback_data=f"challenge:send:{goal_id}:{opponent_id}",
    )
    builder.button(
        text=t(language, "btn.choose_other"),
        callback_data=f"goal:challenge:{goal_id}",
    )
    builder.button(
        text=t(language, "btn.cancel"),
        callback_data=f"goal:view:{goal_id}",
    )

    builder.adjust(1)
    return builder.as_markup()


def incoming_challenge_keyboard(challenge_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "btn.accept"),
        callback_data=f"challenge:accept:{challenge_id}",
    )
    builder.button(
        text=t(language, "btn.decline"),
        callback_data=f"challenge:decline:{challenge_id}",
    )

    builder.adjust(1)
    return builder.as_markup()


def active_challenge_keyboard(challenge_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t(language, "btn.open_challenge"),
        callback_data=f"challenge:view:{challenge_id}",
    )
    builder.adjust(1)
    return builder.as_markup()


def challenge_progress_keyboard(challenge_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t(language, "btn.complete_today_short"),
        callback_data=f"challenge:today:{challenge_id}",
    )
    builder.button(
        text=t(language, "btn.refresh"),
        callback_data=f"challenge:view:{challenge_id}",
    )
    builder.button(
        text=t(language, "btn.back_to_challenge"),
        callback_data=f"challenge:view:{challenge_id}",
    )

    builder.adjust(1)
    return builder.as_markup()


def challenge_history_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(language, "btn.back"), callback_data="challenge:menu")
    builder.adjust(1)
    return builder.as_markup()


def challenge_menu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(language, "btn.create_challenge"), callback_data="challenge:create")
    builder.button(text=t(language, "btn.history"), callback_data="challenge:history")
    builder.adjust(1)
    return builder.as_markup()


def challenge_goals_keyboard(goals, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for goal in goals:
        title = goal.title
        if len(title) > 30:
            title = title[:30] + "..."

        builder.button(
            text=f"🎯 {title}",
            callback_data=f"challenge:goal:{goal.id}",
        )

    builder.button(text=t(language, "btn.back"), callback_data="challenge:menu")
    builder.adjust(1)
    return builder.as_markup()


def challenge_opponents_keyboard(opponents, goal_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for opponent in opponents:
        name = opponent.first_name or opponent.username or t(language, "common.player")
        if len(name) > 20:
            name = name[:20] + "..."

        builder.button(
            text=f"⚔️ {name}",
            callback_data=f"challenge:select:{goal_id}:{opponent.id}",
        )

    builder.button(
        text=t(language, "btn.back_to_challenges"),
        callback_data="challenge:menu",
    )

    builder.adjust(1)
    return builder.as_markup()


def challenge_category_keyboard(goals, language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    used = set((g.category or "other") for g in goals)

    builder.button(
        text=t(language, "btn.filter_all"),
        callback_data="challenge:cat:all",
    )

    for code in CATEGORIES:
        if code in used:
            cat = CATEGORIES[code]
            builder.button(
                text=f"{cat['emoji']} {cat.get(language) or cat['ru']}",
                callback_data=f"challenge:cat:{code}",
            )

    builder.button(text=t(language, "btn.back"), callback_data="challenge:menu")
    builder.adjust(1)
    return builder.as_markup()