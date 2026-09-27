from datetime import datetime, timedelta, timezone
from pathlib import Path

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.bot.keyboards.goals import (
    duration_keyboard,
    goal_preview_keyboard,
    goal_edit_keyboard,
    goals_list_keyboard,
    create_goal_keyboard,
    goal_detail_keyboard,
    steps_keyboard,
    cancel_goal_keyboard,
    category_keyboard,
    description_step_keyboard,
    result_step_keyboard,
    note_skip_keyboard,
)

from app.bot.states.goals import GoalStates
from app.bot.utils.screens import ScreenManager

from app.constants.achievements import achievement_name
from app.constants.categories import category_name
from app.services.achievements import (
    check_and_grant,
    grant_first_step,
    grant_night_owl,
)
from app.services.goal_calc import (
    calculate_rewards,
    calculate_creation_cost,
    calculate_level,
)

from app.database.database import async_session
from app.database.models.user import User
from app.database.models.goal import Goal
from app.database.models.goal_step import GoalStep

from app.locales.texts import t


router = Router()


# ============================================================
# MEDIA
# ============================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
MY_GOALS_IMAGE_RU = MEDIA_DIR / "my_goals_ru.png"
GOAL_COMPLETED_IMAGE_RU = MEDIA_DIR / "goal_completed_ru.png"


# ============================================================
# UTILS
# ============================================================

def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


STEP_XP = 10
STEP_SCORE = 5
GOAL_COMPLETE_XP = 50


async def get_user(session, telegram_id: int):
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


def add_level_up_text(text: str, language: str, level: int) -> str:
    return (
        f"{text}\n\n"
        f"{t(language, 'goals.level_up')}\n"
        f"{t(language, 'goals.new_level')}: <b>{level}</b>"
    )


def difficulty_text(language: str, difficulty: str) -> str:
    if difficulty == "hard":
        return t(language, "goals.difficulty_hard")
    return t(language, "goals.difficulty_normal")


def _preview_text(
    lang: str,
    title: str,
    category: str,
    description: str | None,
    result: str | None,
    duration: int,
    difficulty: str,
    creation_cost: int,
    score_reward: int,
    kick_reward: int,
    balance: int,
) -> str:

    text = (
        f"{t(lang, 'goals.preview')}\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"🎯 <b>{title}</b>\n"
        f"🏷 {category_name(category, lang)}\n\n"
    )
    if description:
        text += f"📝 <i>{description}</i>\n"
    if result:
        text += f"🎯 <i>{result}</i>\n"
    if description or result:
        text += "\n"

    text += (
        f"{t(lang, 'goals.duration_label')}: <b>{duration}</b>\n"
        f"{t(lang, 'goals.difficulty_label')}: "
        f"<b>{difficulty_text(lang, difficulty)}</b>\n\n"
        f"{t(lang, 'goals.conditions')}\n\n"
        f"{t(lang, 'goals.freeze')}: <b>{creation_cost} KICK</b>\n"
        f"⭐ SCORE: <b>+{score_reward}</b>\n"
        f"{t(lang, 'goals.reward')}: <b>+{kick_reward} KICK</b>\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"{t(lang, 'goals.balance')}: <b>{balance} KICK</b>\n\n"
        f"{t(lang, 'goals.cancel_72')}"
    )
    return text


# ============================================================
# MY GOALS  (фото + caption + inline-кнопки)
# ============================================================

@router.message(
    F.text.in_([
        "🎯 Мои цели",
        "🎯 My goals",
        "🎯 Իմ նպատակները",
    ])
)
async def my_goals_handler(message: Message):

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .where(
                Goal.user_id == user.id,
                Goal.status == "active",
            )
            .order_by(Goal.created_at.desc())
        )
        goals = result.scalars().all()

        if not goals:
            text = (
                f"{t(lang, 'goals.title')}\n\n"
                f"{t(lang, 'goals.no_goals')}"
            )
            markup = create_goal_keyboard(lang)
        else:
            text = (
                f"{t(lang, 'goals.title')}\n\n"
                f"{t(lang, 'goals.choose')}\n"
            )
            for goal in goals:
                text += (
                    f"\n{category_name(goal.category, lang)} "
                    f"<b>{goal.title}</b>\n"
                    f"⏱ {goal.duration_days} {t(lang, 'common.days')}\n"
                )
            markup = goals_list_keyboard(goals, lang)

        await ScreenManager.clear_previous(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
        )

        new_message = None

        if MY_GOALS_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                if goals:
                    caption = (
                        f"{t(lang, 'goals.title')}\n\n"
                        f"{t(lang, 'profile.active')}: <b>{len(goals)}</b>\n\n"
                        f"👇"
                    )
                else:
                    caption = (
                        f"{t(lang, 'goals.title')}\n\n"
                        f"{t(lang, 'goals.no_goals')}"
                    )

            try:
                new_message = await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=FSInputFile(MY_GOALS_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        if new_message is None:
            new_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )

        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await message.delete()


# ============================================================
# CREATE GOAL
# ============================================================

@router.callback_query(F.data == "goal:create")
async def create_goal_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.new')}\n\n"
                f"{t(lang, 'goals.choose_duration')}"
            ),
            reply_markup=duration_keyboard(lang),
        )

    await state.set_state(GoalStates.waiting_for_duration)
    await callback.answer()


# ============================================================
# SELECT DURATION
# ============================================================

@router.callback_query(F.data.startswith("duration:"))
async def duration_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    value = callback.data.split(":")[1]

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        if value == "custom":
            await ScreenManager.show(
                bot=callback.bot,
                user=user,
                chat_id=callback.message.chat.id,
                session=session,
                text=(
                    f"{t(lang, 'goals.custom_duration')}\n\n"
                    f"{t(lang, 'goals.enter_days')}"
                ),
            )
            await state.set_state(GoalStates.waiting_for_custom_duration)
            await callback.answer()
            return

        duration = int(value)
        await state.update_data(duration=duration)

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.enter_title')}\n\n"
                f"{t(lang, 'goals.duration_label')}: <b>{duration}</b>"
            ),
        )

    await state.set_state(GoalStates.waiting_for_title)
    await callback.answer()


# ============================================================
# CUSTOM DURATION
# ============================================================

@router.message(GoalStates.waiting_for_custom_duration)
async def custom_duration_handler(
    message: Message,
    state: FSMContext,
):

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        try:
            duration = int(message.text.strip())
        except (ValueError, AttributeError):
            await message.delete()
            await ScreenManager.show(
                bot=message.bot,
                user=user,
                chat_id=message.chat.id,
                session=session,
                text="❌ " + t(lang, "goals.enter_days_number"),
            )
            return

        if duration < 1:
            await message.delete()
            await ScreenManager.show(
                bot=message.bot,
                user=user,
                chat_id=message.chat.id,
                session=session,
                text="❌ " + t(lang, "goals.min_duration"),
            )
            return

        if duration > 365:
            await message.delete()
            await ScreenManager.show(
                bot=message.bot,
                user=user,
                chat_id=message.chat.id,
                session=session,
                text="❌ " + t(lang, "goals.max_duration"),
            )
            return

        await state.update_data(duration=duration)

        await ScreenManager.show(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.enter_title')}\n\n"
                f"{t(lang, 'goals.duration_label')}: <b>{duration}</b>"
            ),
        )

    await state.set_state(GoalStates.waiting_for_title)
    await message.delete()


# ============================================================
# ENTER TITLE → категория
# ============================================================

@router.message(GoalStates.waiting_for_title)
async def goal_title_handler(
    message: Message,
    state: FSMContext,
):

    title = (message.text or "").strip()
    await message.delete()

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        if not title:
            await ScreenManager.show(
                bot=message.bot,
                user=user,
                chat_id=message.chat.id,
                session=session,
                text="❌ " + t(lang, "goals.title_empty"),
            )
            return

        if len(title) > 500:
            await ScreenManager.show(
                bot=message.bot,
                user=user,
                chat_id=message.chat.id,
                session=session,
                text="❌ " + t(lang, "goals.title_too_long"),
            )
            return

        await state.update_data(title=title)

        await ScreenManager.show(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'category.title')}\n\n"
                f"{t(lang, 'category.hint')}"
            ),
            reply_markup=category_keyboard(lang),
        )

    await state.set_state(GoalStates.choosing_category)


# ============================================================
# CATEGORY → описание
# ============================================================

@router.callback_query(
    GoalStates.choosing_category,
    F.data.startswith("goal:category:"),
)
async def category_select_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    code = callback.data.split(":")[2]
    await state.update_data(category=code)

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=t(lang, "goals.enter_description"),
            reply_markup=description_step_keyboard(lang),
        )

    await state.set_state(GoalStates.waiting_for_description)
    await callback.answer()


# ============================================================
# DESCRIPTION → result → preview
# ============================================================

async def _show_preview(bot, user, chat_id, session, state):
    lang = user.language or "ru"
    data = await state.get_data()

    duration = data.get("duration")
    title = data.get("title")
    category = data.get("category", "other")
    description = data.get("description")
    result = data.get("result")

    difficulty, score_reward, kick_reward = calculate_rewards(duration)
    creation_cost = calculate_creation_cost(duration)

    text = _preview_text(
        lang, title, category, description, result, duration,
        difficulty, creation_cost, score_reward, kick_reward,
        user.balance,
    )

    await ScreenManager.show(
        bot=bot,
        user=user,
        chat_id=chat_id,
        session=session,
        text=text,
        reply_markup=goal_preview_keyboard(lang),
    )


@router.message(GoalStates.waiting_for_description)
async def description_handler(message: Message, state: FSMContext):
    desc = (message.text or "").strip()[:1000] or None
    await message.delete()

    await state.update_data(description=desc)

    async with async_session() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            return
        lang = user.language or "ru"

        await ScreenManager.show(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
            text=t(lang, "goals.enter_result"),
            reply_markup=result_step_keyboard(lang),
        )

    await state.set_state(GoalStates.waiting_for_result)


@router.callback_query(F.data == "goal:desc:skip")
async def desc_skip_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(description=None)

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=t(lang, "goals.enter_result"),
            reply_markup=result_step_keyboard(lang),
        )

    await state.set_state(GoalStates.waiting_for_result)
    await callback.answer()


@router.message(GoalStates.waiting_for_result)
async def result_handler(message: Message, state: FSMContext):
    res = (message.text or "").strip()[:1000] or None
    await message.delete()

    await state.update_data(result=res)

    async with async_session() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            return
        await _show_preview(
            message.bot, user, message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)


@router.callback_query(F.data == "goal:result:skip")
async def result_skip_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(result=None)

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        await _show_preview(
            callback.bot, user, callback.message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)
    await callback.answer()


# ============================================================
# START GOAL
# ============================================================

@router.callback_query(F.data == "goal:start")
async def start_goal_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    data = await state.get_data()
    duration = data.get("duration")
    title = data.get("title")
    category = data.get("category", "other")
    description = data.get("description")

    if not duration or not title:
        await callback.answer(t("ru", "goals.data_lost"), show_alert=True)
        return

    creation_cost = calculate_creation_cost(duration)
    difficulty, score_reward, kick_reward = calculate_rewards(duration)

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        if user.balance < creation_cost:
            await ScreenManager.show(
                bot=callback.bot,
                user=user,
                chat_id=callback.message.chat.id,
                session=session,
                text=(
                    f"{t(lang, 'goals.insufficient_kick')}\n\n"
                    f"{t(lang, 'goals.need_kick')} "
                    f"<b>{creation_cost} KICK</b>.\n\n"
                    f"{t(lang, 'goals.balance')}: <b>{user.balance} KICK</b>"
                ),
            )
            await callback.answer(
                t(lang, "goals.insufficient_kick"),
                show_alert=True,
            )
            return

        start_date = utcnow()
        deadline = start_date + timedelta(days=duration)

        goal = Goal(
            user_id=user.id,
            title=title,
            description=description,
            category=category,
            duration_days=duration,
            difficulty=difficulty,
            score_reward=score_reward,
            kick_reward=kick_reward,
            start_date=start_date,
            deadline=deadline,
            status="active",
            result=data.get("result"),
            missed_days_streak=0,
        )
        session.add(goal)
        await session.flush()

        for day in range(1, duration + 1):
            session.add(
                GoalStep(
                    goal_id=goal.id,
                    day_number=day,
                    title=f"Day {day}",
                    status="pending",
                )
            )

        user.balance -= creation_cost
        user.frozen_kick += creation_cost

        await session.commit()
        await state.clear()

        text = (
            f"{t(lang, 'goals.started')}\n\n"
            f"{category_name(category, lang)} <b>{goal.title}</b>\n\n"
            f"{t(lang, 'goals.duration_label')}: "
            f"<b>{goal.duration_days}</b>\n\n"
            f"{t(lang, 'goals.frozen')}: "
            f"<b>{creation_cost} KICK</b>\n"
            f"⭐ SCORE: <b>+{goal.score_reward}</b>\n"
            f"{t(lang, 'goals.reward')}: "
            f"<b>+{goal.kick_reward} KICK</b>\n\n"
            f"{t(lang, 'goals.first_step_wait')}\n\n"
            f"{t(lang, 'goals.remember_cancel')}"
        )

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=text,
            reply_markup=goal_detail_keyboard(
                goal_id=goal.id,
                can_cancel=True,
                language=lang,
            ),
        )

    await callback.answer("🚀")


# ============================================================
# GOAL EDIT MENU
# ============================================================

@router.callback_query(F.data == "goal:edit")
async def edit_goal_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.editing')}\n\n"
                f"{t(lang, 'goals.what_edit')}"
            ),
            reply_markup=goal_edit_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "goal:edit:result")
async def edit_result_handler(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.new_result')}\n\n"
                f"{t(lang, 'goals.enter_new_result')}"
            ),
        )

    await state.set_state(GoalStates.editing_result)
    await callback.answer()


@router.message(GoalStates.editing_result)
async def save_edited_result_handler(message: Message, state: FSMContext):
    res = (message.text or "").strip()[:1000] or None
    await message.delete()

    await state.update_data(result=res)

    async with async_session() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            return
        await _show_preview(
            message.bot, user, message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)


@router.callback_query(F.data == "goal:edit:category")
async def edit_category_handler(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'category.title')}\n\n"
                f"{t(lang, 'category.hint')}"
            ),
            reply_markup=category_keyboard(lang),
        )

    await state.set_state(GoalStates.choosing_category)
    await callback.answer()


# ============================================================
# EDIT TITLE
# ============================================================

@router.callback_query(F.data == "goal:edit:title")
async def edit_title_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.new_title')}\n\n"
                f"{t(lang, 'goals.enter_new_title')}"
            ),
        )

    await state.set_state(GoalStates.editing_title)
    await callback.answer()


@router.message(GoalStates.editing_title)
async def save_edited_title_handler(
    message: Message,
    state: FSMContext,
):

    title = (message.text or "").strip()
    await message.delete()

    if not title:
        return

    await state.update_data(title=title)

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        await _show_preview(
            message.bot, user, message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)


# ============================================================
# EDIT DESCRIPTION
# ============================================================

@router.callback_query(F.data == "goal:edit:description")
async def edit_description_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.new_description')}\n\n"
                f"{t(lang, 'goals.enter_new_description')}"
            ),
        )

    await state.set_state(GoalStates.editing_description)
    await callback.answer()


@router.message(GoalStates.editing_description)
async def save_edited_description_handler(
    message: Message,
    state: FSMContext,
):

    desc = (message.text or "").strip()[:1000] or None
    await message.delete()

    await state.update_data(description=desc)

    async with async_session() as session:

        user = await get_user(session, message.from_user.id)
        if not user:
            return

        await _show_preview(
            message.bot, user, message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)


# ============================================================
# EDIT DURATION
# ============================================================

@router.callback_query(F.data == "goal:edit:duration")
async def edit_duration_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.new_duration')}\n\n"
                f"{t(lang, 'goals.choose_new_duration')}"
            ),
            reply_markup=duration_keyboard(lang),
        )

    await state.set_state(GoalStates.editing_duration)
    await callback.answer()


@router.callback_query(
    GoalStates.editing_duration,
    F.data.startswith("duration:"),
)
async def edit_duration_select_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    value = callback.data.split(":")[1]

    if value == "custom":
        async with async_session() as session:
            user = await get_user(session, callback.from_user.id)
            if not user:
                return
            lang = user.language or "ru"
            await ScreenManager.show(
                bot=callback.bot,
                user=user,
                chat_id=callback.message.chat.id,
                session=session,
                text=(
                    f"{t(lang, 'goals.custom_duration')}\n\n"
                    f"{t(lang, 'goals.enter_days')}"
                ),
            )
        await state.set_state(GoalStates.editing_custom_duration)
        await callback.answer()
        return

    duration = int(value)
    await state.update_data(duration=duration)

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        await _show_preview(
            callback.bot, user, callback.message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)
    await callback.answer()


@router.message(GoalStates.editing_custom_duration)
async def edit_custom_duration_handler(
    message: Message,
    state: FSMContext,
):

    try:
        duration = int(message.text.strip())
    except (ValueError, AttributeError):
        await message.delete()
        return

    if duration < 1 or duration > 365:
        await message.delete()
        return

    await message.delete()
    await state.update_data(duration=duration)

    async with async_session() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            return
        await _show_preview(
            message.bot, user, message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)


@router.callback_query(F.data == "goal:edit:back")
async def edit_back_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        data = await state.get_data()
        if not data.get("duration") or not data.get("title"):
            await callback.answer()
            return
        await _show_preview(
            callback.bot, user, callback.message.chat.id, session, state,
        )

    await state.set_state(GoalStates.preview)
    await callback.answer()


# ============================================================
# CANCEL CREATION
# ============================================================

@router.callback_query(F.data == "goal:cancel")
async def cancel_creation_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    await state.clear()

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        lang = user.language or "ru"
        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.creation_cancelled')}\n\n"
                f"{t(lang, 'goals.can_create_again')}"
            ),
        )

    await callback.answer()


# ============================================================
# VIEW GOAL
# ============================================================

@router.callback_query(F.data.startswith("goal:view:"))
async def view_goal_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(Goal.id == goal_id, Goal.user_id == user.id)
        )
        goal = result.scalar_one_or_none()

        if not goal:
            await callback.answer(
                t(lang, "common.goal_not_found"), show_alert=True,
            )
            return

        total = len(goal.steps)
        done = sum(1 for s in goal.steps if s.status == "completed")
        pct = int(done / total * 100) if total else 0

        creation_cost = calculate_creation_cost(goal.duration_days)

        can_cancel = False
        if goal.status == "active":
            cancel_deadline = goal.start_date + timedelta(hours=72)
            can_cancel = utcnow() <= cancel_deadline

        status_text = {
            "active": t(lang, "goals.status_active"),
            "completed": t(lang, "goals.status_completed"),
            "cancelled": t(lang, "goals.status_cancelled"),
            "failed": t(lang, "goals.status_failed"),
        }.get(goal.status, goal.status)

        text = (
            f"{category_name(goal.category, lang)} "
            f"<b>{goal.title}</b>\n\n"
            f"📌 {status_text}\n"
        )
        if goal.description:
            text += f"📝 <i>{goal.description}</i>\n\n"

        text += (
            f"{t(lang, 'goals.duration_label')}: "
            f"<b>{goal.duration_days}</b>\n\n"
            f"{t(lang, 'goals.progress')}: <b>{pct}%</b>\n"
            f"{t(lang, 'goals.completed')}: <b>{done}/{total}</b>\n\n"
            f"{t(lang, 'goals.frozen')}: "
            f"<b>{creation_cost} KICK</b>\n"
            f"⭐ SCORE: <b>+{goal.score_reward}</b>\n"
            f"{t(lang, 'goals.reward')}: "
            f"<b>+{goal.kick_reward} KICK</b>"
        )

        if goal.result:
            text += f"🎯 <i>{goal.result}</i>\n\n"

        if goal.status == "active":
            remaining = goal.start_date + timedelta(hours=72) - utcnow()
            if remaining.total_seconds() > 0:
                hours = int(remaining.total_seconds() // 3600)
                text += (
                    f"\n\n{t(lang, 'goals.cancel_available')} "
                    f"<b>{hours} {t(lang, 'common.hours_short')}</b>"
                )
            else:
                text += f"\n\n{t(lang, 'goals.cancel_unavailable')}"

        if goal.status == "active" and goal.missed_days_streak == 1:
            text += f"\n\n{t(lang, 'goals.missed_warning_1')}"
        elif goal.status == "failed":
            text += f"\n\n{t(lang, 'goals.missed_warning_2')}"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=text,
            reply_markup=goal_detail_keyboard(
                goal_id=goal.id,
                can_cancel=can_cancel,
                language=lang,
            ),
        )

    await callback.answer()


# ============================================================
# COMPLETE TODAY
# ============================================================

@router.callback_query(F.data.startswith("goal:today:"))
async def complete_today_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()

        if not goal:
            await callback.answer(
                t(lang, "goals.active_not_found"), show_alert=True,
            )
            return

        now = utcnow()
        minimum_first_step_time = goal.start_date + timedelta(hours=1)

        if now < minimum_first_step_time:
            remaining = minimum_first_step_time - now
            total_seconds = int(remaining.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            await callback.answer(
                f"{t(lang, 'goals.first_step_unavailable')} "
                f"{hours} {t(lang, 'common.hours_short')} "
                f"{minutes} {t(lang, 'common.minutes_short')}.",
                show_alert=True,
            )
            return

        elapsed = now - goal.start_date
        current_day = max(1, min(elapsed.days + 1, goal.duration_days))

        current_step = next(
            (s for s in goal.steps if s.day_number == current_day),
            None,
        )

        if not current_step:
            await callback.answer(
                t(lang, "goals.step_not_found"), show_alert=True,
            )
            return

        if current_step.status == "completed":
            await callback.answer(
                t(lang, "goals.step_already_done"), show_alert=True,
            )
            return

        await state.update_data(
            note_goal_id=goal.id,
            note_step_id=current_step.id,
        )

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.note_title')}\n\n"
                f"{t(lang, 'goals.note_hint')}"
            ),
            reply_markup=note_skip_keyboard(lang),
        )

    await state.set_state(GoalStates.waiting_for_step_note)
    await callback.answer()


# ============================================================
# ФИНАЛИЗАЦИЯ ШАГА
# ============================================================

async def _finalize_step(bot, user, session, goal_id: int, note: str | None):

    lang = user.language or "ru"

    result = await session.execute(
        select(Goal)
        .options(selectinload(Goal.steps))
        .where(
            Goal.id == goal_id,
            Goal.user_id == user.id,
            Goal.status == "active",
        )
    )
    goal = result.scalar_one_or_none()
    if not goal:
        return

    now = utcnow()
    elapsed = now - goal.start_date
    current_day = max(1, min(elapsed.days + 1, goal.duration_days))

    step = next((s for s in goal.steps if s.day_number == current_day), None)
    if not step or step.status == "completed":
        return

    step.status = "completed"
    step.completed_at = now
    step.note = note

    goal.missed_days_streak = 0
    goal.warning_sent_at = None

    await grant_first_step(session, user.id)
    if now.hour >= 22 or now.hour < 5:
        await grant_night_owl(session, user.id)

    user.xp += STEP_XP
    user.score += STEP_SCORE
    user.level = calculate_level(user.xp)

    today = now.date()
    last = user.last_activity_date.date() if user.last_activity_date else None
    if last != today:
        if last and (today - last).days == 1:
            user.current_streak += 1
        else:
            user.current_streak = 1
        if user.current_streak > user.best_streak:
            user.best_streak = user.current_streak
        user.last_activity_date = now

    new_achievements = await check_and_grant(session, user)

    completed = sum(1 for s in goal.steps if s.status == "completed")
    total = len(goal.steps)
    goal_completed = completed >= total

    completion_reward = 0

    if goal_completed:
        goal.status = "completed"
        creation_cost = calculate_creation_cost(goal.duration_days)
        user.frozen_kick = max(0, user.frozen_kick - creation_cost)
        user.balance += creation_cost + goal.kick_reward
        user.score += goal.score_reward
        user.xp += GOAL_COMPLETE_XP
        user.level = calculate_level(user.xp)
        completion_reward = goal.kick_reward

        new_achievements += await check_and_grant(session, user)

    await session.commit()

    # --- Текст ---
    if goal_completed:
        text = (
            f"{t(lang, 'goals.completed_title')}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🎯 <b>{goal.title}</b>\n\n"
            f"{t(lang, 'goals.all_steps_done')}\n\n"
            f"{t(lang, 'goals.step_reward')}: "
            f"<b>+{completion_reward} KICK</b>\n"
            f"⭐ SCORE: <b>+{goal.score_reward}</b>\n"
            f"{t(lang, 'goals.xp')}: <b>+{GOAL_COMPLETE_XP}</b>\n\n"
            f"{t(lang, 'goals.balance')}: <b>{user.balance} KICK</b>"
        )
        can_cancel = False
    else:
        text = (
            f"{t(lang, 'goals.step_completed')}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🎯 <b>{goal.title}</b>\n\n"
            f"{t(lang, 'goals.day')}: <b>{current_day}</b>\n\n"
            f"{t(lang, 'goals.xp')}: <b>+{STEP_XP}</b>\n"
            f"⭐ SCORE: <b>+{STEP_SCORE}</b>\n\n"
            f"{t(lang, 'goals.progress')}: "
            f"<b>{completed}/{total}</b>"
        )
        cancel_deadline = goal.start_date + timedelta(hours=72)
        can_cancel = utcnow() <= cancel_deadline

    if new_achievements:
        text += f"\n\n🎉 <b>{t(lang, 'ach.new_title').replace('<b>', '').replace('</b>', '')}</b>\n"
        for code in new_achievements:
            text += f"\n{achievement_name(code, lang)}"

    # --- Удаляем предыдущий экран ---
    await ScreenManager.clear_previous(
        bot=bot,
        user=user,
        chat_id=user.telegram_id,
        session=session,
    )

    new_message = None

    # --- Если цель завершена и есть картинка — отправляем с фото ---
    if goal_completed and GOAL_COMPLETED_IMAGE_RU.exists():

        if len(text) <= 1024:
            caption = text
        else:
            caption = (
                f"{t(lang, 'goals.completed_title')}\n\n"
                f"🎯 <b>{goal.title}</b>\n\n"
                f"{t(lang, 'goals.all_steps_done')}\n\n"
                f"{t(lang, 'goals.step_reward')}: "
                f"<b>+{completion_reward} KICK</b>\n"
                f"⭐ SCORE: <b>+{goal.score_reward}</b>"
            )

        try:
            new_message = await bot.send_photo(
                chat_id=user.telegram_id,
                photo=FSInputFile(GOAL_COMPLETED_IMAGE_RU),
                caption=caption,
                parse_mode="HTML",
                reply_markup=goal_detail_keyboard(goal.id, can_cancel, lang),
            )
        except Exception:
            new_message = None

    # --- Фолбэк ---
    if new_message is None:
        new_message = await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            parse_mode="HTML",
            reply_markup=goal_detail_keyboard(goal.id, can_cancel, lang),
        )

    user.last_bot_message_id = new_message.message_id
    await session.commit()


@router.message(GoalStates.waiting_for_step_note)
async def note_handler(message: Message, state: FSMContext):

    note = (message.text or "").strip()[:1000] or None
    await message.delete()

    data = await state.get_data()
    goal_id = data.get("note_goal_id")

    if not goal_id:
        await state.clear()
        return

    async with async_session() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            return
        await _finalize_step(message.bot, user, session, goal_id, note)

    await state.clear()


@router.callback_query(F.data == "goal:today:skip_note")
async def skip_note_handler(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    goal_id = data.get("note_goal_id")

    if not goal_id:
        await callback.answer()
        return

    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            return
        await _finalize_step(callback.bot, user, session, goal_id, None)

    await state.clear()
    await callback.answer()


# ============================================================
# HEATMAP
# ============================================================

@router.callback_query(F.data.startswith("goal:heatmap:"))
async def heatmap_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(Goal.id == goal_id, Goal.user_id == user.id)
        )
        goal = result.scalar_one_or_none()
        if not goal:
            await callback.answer(
                t(lang, "common.goal_not_found"), show_alert=True,
            )
            return

        steps = sorted(goal.steps, key=lambda s: s.day_number)

        lines = [
            f"{t(lang, 'goals.heatmap_title')}\n",
            f"🎯 <b>{goal.title}</b>\n",
        ]

        row = ""
        for i, step in enumerate(steps, start=1):
            if step.status == "completed":
                row += "🟩"
            elif step.status == "missed":
                row += "🟥"
            else:
                row += "⬜"
            if i % 10 == 0:
                lines.append(row)
                row = ""

        if row:
            lines.append(row)

        lines.append("")
        lines.append(f"🟩 {t(lang, 'goals.heatmap_done')}")
        lines.append(f"🟥 {t(lang, 'goals.heatmap_missed')}")
        lines.append(f"⬜ {t(lang, 'goals.heatmap_pending')}")

        await callback.message.edit_text(
            "\n".join(lines),
            parse_mode="HTML",
            reply_markup=goal_detail_keyboard(goal.id, False, lang),
        )

    await callback.answer()


# ============================================================
# SHOW ALL STEPS
# ============================================================

@router.callback_query(F.data.startswith("goal:steps:"))
async def show_all_steps_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(Goal.id == goal_id, Goal.user_id == user.id)
        )
        goal = result.scalar_one_or_none()

        if not goal:
            await callback.answer(
                t(lang, "common.goal_not_found"), show_alert=True,
            )
            return

        steps = sorted(goal.steps, key=lambda s: s.day_number)

        text = (
            f"{t(lang, 'goals.steps')}\n\n"
            f"🎯 <b>{goal.title}</b>\n\n"
        )

        for step in steps:
            if step.status == "completed":
                icon = "✅"
            elif step.status == "missed":
                icon = "🟥"
            else:
                icon = "⬜"

            text += (
                f"{icon} {t(lang, 'goals.day_word')} "
                f"<b>{step.day_number}</b>\n"
            )
            if step.note:
                text += f"    📝 <i>{step.note}</i>\n"

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=text,
            reply_markup=steps_keyboard(goal.id, lang),
        )

    await callback.answer()


# ============================================================
# CANCEL GOAL
# ============================================================

@router.callback_query(F.data.startswith("goal:cancel_goal:"))
async def cancel_goal_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal).where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()

        if not goal:
            await callback.answer(
                t(lang, "common.goal_not_found"), show_alert=True,
            )
            return

        cancel_deadline = goal.start_date + timedelta(hours=72)

        if utcnow() > cancel_deadline:
            await ScreenManager.show(
                bot=callback.bot,
                user=user,
                chat_id=callback.message.chat.id,
                session=session,
                text=(
                    f"{t(lang, 'goals.cancel_unavailable_title')}\n\n"
                    f"{t(lang, 'goals.cancel_72_passed')}"
                ),
                reply_markup=goal_detail_keyboard(
                    goal.id, False, lang,
                ),
            )
            await callback.answer()
            return

        creation_cost = calculate_creation_cost(goal.duration_days)

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.cancel_confirm')}\n\n"
                f"🎯 <b>{goal.title}</b>\n\n"
                f"{t(lang, 'goals.returned')}: "
                f"<b>{creation_cost} KICK</b>\n\n"
                f"{t(lang, 'goals.cancel_info')}"
            ),
            reply_markup=cancel_goal_keyboard(goal.id, lang),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("goal:confirm_cancel:"))
async def confirm_cancel_goal_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal).where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()

        if not goal:
            await callback.answer(
                t(lang, "goals.already_cancelled"), show_alert=True,
            )
            return

        cancel_deadline = goal.start_date + timedelta(hours=72)

        if utcnow() > cancel_deadline:
            await ScreenManager.show(
                bot=callback.bot,
                user=user,
                chat_id=callback.message.chat.id,
                session=session,
                text=(
                    f"{t(lang, 'goals.too_late')}\n\n"
                    f"{t(lang, 'goals.too_late_text')}"
                ),
                reply_markup=goal_detail_keyboard(
                    goal.id, False, lang,
                ),
            )
            await callback.answer()
            return

        creation_cost = calculate_creation_cost(goal.duration_days)

        if user.frozen_kick < creation_cost:
            await ScreenManager.show(
                bot=callback.bot,
                user=user,
                chat_id=callback.message.chat.id,
                session=session,
                text=(
                    f"{t(lang, 'goals.balance_error')}\n\n"
                    f"{t(lang, 'goals.balance_error_text')}"
                ),
            )
            await callback.answer()
            return

        user.frozen_kick -= creation_cost
        user.balance += creation_cost

        goal.status = "cancelled"
        await session.commit()

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"{t(lang, 'goals.cancelled')}\n\n"
                f"🎯 <b>{goal.title}</b>\n\n"
                f"{t(lang, 'goals.refunded')}: "
                f"<b>{creation_cost} KICK</b>\n\n"
                f"{t(lang, 'goals.available')}: "
                f"<b>{user.balance} KICK</b>\n"
                f"{t(lang, 'goals.in_goals')}: "
                f"<b>{user.frozen_kick} KICK</b>"
            ),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("goal:cancel_back:"))
async def cancel_back_handler(callback: CallbackQuery):

    goal_id = int(callback.data.split(":")[2])

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .options(selectinload(Goal.steps))
            .where(
                Goal.id == goal_id,
                Goal.user_id == user.id,
                Goal.status == "active",
            )
        )
        goal = result.scalar_one_or_none()

        if not goal:
            await callback.answer(
                t(lang, "common.goal_not_found"), show_alert=True,
            )
            return

        total = len(goal.steps)
        done = sum(1 for s in goal.steps if s.status == "completed")
        pct = int(done / total * 100) if total else 0

        creation_cost = calculate_creation_cost(goal.duration_days)
        cancel_deadline = goal.start_date + timedelta(hours=72)
        can_cancel = utcnow() <= cancel_deadline

        await ScreenManager.show(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
            text=(
                f"🎯 <b>{goal.title}</b>\n\n"
                f"{t(lang, 'goals.duration_label')}: "
                f"<b>{goal.duration_days}</b>\n"
                f"{t(lang, 'goals.progress')}: <b>{pct}%</b>\n\n"
                f"{t(lang, 'goals.frozen')}: "
                f"<b>{creation_cost} KICK</b>\n"
                f"⭐ SCORE: <b>+{goal.score_reward}</b>\n"
                f"{t(lang, 'goals.reward')}: "
                f"<b>+{goal.kick_reward} KICK</b>\n\n"
                f"{t(lang, 'goals.continue')}"
            ),
            reply_markup=goal_detail_keyboard(goal.id, can_cancel, lang),
        )

    await callback.answer()


# ============================================================
# BACK TO GOALS LIST  (с фото)
# ============================================================

@router.callback_query(F.data == "goal:list")
async def back_to_goals_list_handler(callback: CallbackQuery):

    async with async_session() as session:

        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer()
            return

        lang = user.language or "ru"

        result = await session.execute(
            select(Goal)
            .where(
                Goal.user_id == user.id,
                Goal.status == "active",
            )
            .order_by(Goal.created_at.desc())
        )
        goals = result.scalars().all()

        if not goals:
            text = (
                f"{t(lang, 'goals.title')}\n\n"
                f"{t(lang, 'goals.no_goals')}"
            )
            markup = create_goal_keyboard(lang)
        else:
            text = (
                f"{t(lang, 'goals.title')}\n\n"
                f"{t(lang, 'goals.choose')}\n"
            )
            for goal in goals:
                text += (
                    f"\n{category_name(goal.category, lang)} "
                    f"<b>{goal.title}</b>\n"
                    f"⏱ {goal.duration_days} {t(lang, 'common.days')}\n"
                )
            markup = goals_list_keyboard(goals, lang)

        await ScreenManager.clear_previous(
            bot=callback.bot,
            user=user,
            chat_id=callback.message.chat.id,
            session=session,
        )

        new_message = None

        if MY_GOALS_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                caption = (
                    f"{t(lang, 'goals.title')}\n\n"
                    f"👇"
                )

            try:
                new_message = await callback.bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=FSInputFile(MY_GOALS_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        if new_message is None:
            new_message = await callback.bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )

        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await callback.answer()