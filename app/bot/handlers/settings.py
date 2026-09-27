from pathlib import Path

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile

from sqlalchemy import delete, select

from app.bot.keyboards.main import main_menu
from app.bot.keyboards.settings import (
    confirm_delete_goals_keyboard,
    confirm_reset_progress_keyboard,
    data_keyboard,
    language_keyboard,
    notifications_keyboard,
    settings_keyboard,
)
from app.bot.utils.safe_edit import safe_edit
from app.bot.utils.screens import ScreenManager
from app.database.database import async_session
from app.database.models.challenge import Challenge
from app.database.models.goal import Goal
from app.database.models.user import User
from app.locales.texts import t

router = Router()

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
SETTINGS_IMAGE_RU = MEDIA_DIR / "settings_ru.png"


# ⚙️ Открыть настройки
@router.message(
    F.text.in_([
        "⚙️ Настройки",
        "⚙️ Settings",
        "⚙️ Կարգավորումներ",
    ])
)
async def settings_handler(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            return

        lang = user.language or "ru"

        text = f"{t(lang, 'settings.title')}\n\n{t(lang, 'settings.choose')}"
        markup = settings_keyboard(lang)

        # --- Удаляем предыдущий экран ---
        await ScreenManager.clear_previous(
            bot=message.bot,
            user=user,
            chat_id=message.chat.id,
            session=session,
        )

        new_message = None

        # --- Фото для всех языков ---
        if SETTINGS_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                caption = (
                    f"⚙️ <b>SETTINGS</b>\n\n"
                    f"👇"
                )

            try:
                new_message = await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=FSInputFile(SETTINGS_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        # --- Фолбэк ---
        if new_message is None:
            new_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )

        # --- Запоминаем сообщение ---
        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await message.delete()


# 🔔 Уведомления
@router.callback_query(F.data == "settings:notifications")
async def notifications_handler(callback: CallbackQuery):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer(t("ru", "common.user_not_found"), show_alert=True)
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.notifications_title"),
            reply_markup=notifications_keyboard(
                language=lang,
                goal_notifications=user.goal_notifications,
                challenge_notifications=user.challenge_notifications,
                achievement_notifications=user.achievement_notifications,
            ),
        )

    await callback.answer()


# Переключатели уведомлений
@router.callback_query(F.data == "settings:toggle_goal_notifications")
async def toggle_goal_notifications(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        user.goal_notifications = not user.goal_notifications
        await session.commit()

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.notifications_title"),
            reply_markup=notifications_keyboard(
                language=lang,
                goal_notifications=user.goal_notifications,
                challenge_notifications=user.challenge_notifications,
                achievement_notifications=user.achievement_notifications,
            ),
        )

    await callback.answer()


@router.callback_query(F.data == "settings:toggle_challenge_notifications")
async def toggle_challenge_notifications(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        user.challenge_notifications = not user.challenge_notifications
        await session.commit()

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.notifications_title"),
            reply_markup=notifications_keyboard(
                language=lang,
                goal_notifications=user.goal_notifications,
                challenge_notifications=user.challenge_notifications,
                achievement_notifications=user.achievement_notifications,
            ),
        )

    await callback.answer()


@router.callback_query(F.data == "settings:toggle_achievement_notifications")
async def toggle_achievement_notifications(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        user.achievement_notifications = not user.achievement_notifications
        await session.commit()

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.notifications_title"),
            reply_markup=notifications_keyboard(
                language=lang,
                goal_notifications=user.goal_notifications,
                challenge_notifications=user.challenge_notifications,
                achievement_notifications=user.achievement_notifications,
            ),
        )

    await callback.answer()


# 🌐 Язык
@router.callback_query(F.data == "settings:language")
async def language_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.choose_language"),
            reply_markup=language_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("language:"))
async def change_language(callback: CallbackQuery):

    language = callback.data.split(":")[1]
    if language not in ("ru", "en", "hy"):
        await callback.answer("?", show_alert=True)
        return

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        user.language = language
        await session.commit()

        # Обновляем reply-клавиатуру на новом языке
        try:
            await callback.bot.send_message(
                chat_id=callback.message.chat.id,
                text=t(language, "settings.language_changed"),
                reply_markup=main_menu(language),
                parse_mode="HTML",
            )
        except Exception:
            pass

        # Обновляем экран настроек
        await safe_edit(
            callback.message,
            f"{t(language, 'settings.title')}\n\n{t(language, 'settings.choose')}",
            reply_markup=settings_keyboard(language),
        )

    await callback.answer()


# 🗑 Данные
@router.callback_query(F.data == "settings:data")
async def data_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            f"{t(lang, 'settings.data_title')}\n\n{t(lang, 'settings.data_description')}",
            reply_markup=data_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "settings:back")
async def settings_back_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            f"{t(lang, 'settings.title')}\n\n{t(lang, 'settings.choose')}",
            reply_markup=settings_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "settings:main_menu")
async def settings_main_menu_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        try:
            await callback.message.delete()
        except Exception:
            pass

        new_message = await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=t(lang, "settings.main_menu_text"),
            reply_markup=main_menu(lang),
        )

        user.last_bot_message_id = new_message.message_id
        await session.commit()

    await callback.answer()


# 🗑 Удаление целей
@router.callback_query(F.data == "data:delete_goals")
async def delete_goals_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.delete_goals_warning"),
            reply_markup=confirm_delete_goals_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "data:confirm_delete_goals")
async def confirm_delete_goals_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        goals_result = await session.execute(
            select(Goal.id).where(Goal.user_id == user.id)
        )
        goal_ids = goals_result.scalars().all()

        if goal_ids:
            await session.execute(
                delete(Challenge).where(Challenge.goal_id.in_(goal_ids))
            )
            await session.execute(
                delete(Goal).where(Goal.id.in_(goal_ids))
            )

        await session.commit()

        await safe_edit(
            callback.message,
            f"{t(lang, 'settings.goals_deleted')}\n\n"
            f"{t(lang, 'settings.data_title')}\n\n"
            f"{t(lang, 'settings.data_description')}",
            reply_markup=data_keyboard(lang),
        )

    await callback.answer()


# 🔄 Сброс прогресса
@router.callback_query(F.data == "data:reset_progress")
async def reset_progress_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            t(lang, "settings.reset_progress_warning"),
            reply_markup=confirm_reset_progress_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "data:confirm_reset_progress")
async def confirm_reset_progress_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        user.score = 0
        user.xp = 0
        user.level = 1
        user.current_streak = 0
        user.best_streak = 0
        user.last_activity_date = None

        await session.commit()

        await safe_edit(
            callback.message,
            f"{t(lang, 'settings.progress_reset')}\n\n"
            f"{t(lang, 'settings.data_title')}\n\n"
            f"{t(lang, 'settings.data_description')}",
            reply_markup=data_keyboard(lang),
        )

    await callback.answer()


@router.callback_query(F.data == "data:cancel")
async def data_cancel_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            await callback.answer()
            return

        lang = user.language or "ru"

        await safe_edit(
            callback.message,
            f"{t(lang, 'settings.data_title')}\n\n{t(lang, 'settings.data_description')}",
            reply_markup=data_keyboard(lang),
        )

    await callback.answer()