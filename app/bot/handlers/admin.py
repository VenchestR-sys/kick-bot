from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy import select, func

from app.config.admins import is_admin
from app.bot.keyboards.admin import (
    admin_menu_keyboard,
    admin_back_keyboard,
    admin_users_keyboard,
    admin_user_keyboard,
)
from app.database.database import async_session
from app.database.models.user import User
from app.database.models.goal import Goal
from app.database.models.challenge import Challenge
from app.database.models.achievement import UserAchievement


router = Router()

PAGE_SIZE = 10


class AdminStates(StatesGroup):
    waiting_for_user_query = State()
    waiting_for_grant = State()
    waiting_for_ban = State()
    waiting_for_broadcast = State()


def _is_admin(telegram_id: int) -> bool:
    return is_admin(telegram_id)


# =========================================================
# ОБЩАЯ ФУНКЦИЯ: ТЕКСТ КАРТОЧКИ ЮЗЕРА
# =========================================================

async def _build_user_text(session, user: User) -> str:

    goals_active = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id, Goal.status == "active"
        )
    )).scalar() or 0

    goals_done = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id, Goal.status == "completed"
        )
    )).scalar() or 0

    ach = (await session.execute(
        select(func.count(UserAchievement.id)).where(
            UserAchievement.user_id == user.id
        )
    )).scalar() or 0

    return (
        f"👤 <b>{user.first_name or '—'}</b>\n"
        f"🆔 <code>{user.telegram_id}</code>\n"
        f"@{user.username or '—'}\n\n"
        f"🪙 Баланс: <b>{user.balance}</b>\n"
        f"🔒 Заморожено: <b>{user.frozen_kick}</b>\n"
        f"⭐ SCORE: <b>{user.score}</b>\n"
        f"⚡ XP: <b>{user.xp}</b>\n"
        f"🏆 Уровень: <b>{user.level}</b>\n"
        f"🔥 Streak: <b>{user.current_streak}</b> "
        f"(рекорд: {user.best_streak})\n\n"
        f"🎯 Активных целей: <b>{goals_active}</b>\n"
        f"🏆 Завершено: <b>{goals_done}</b>\n"
        f"🥇 Достижений: <b>{ach}</b>\n\n"
        f"🌐 Язык: <b>{user.language}</b>"
    )


# =========================================================
# ENTRY
# =========================================================

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not _is_admin(message.from_user.id):
        return

    await message.answer(
        "🛠 <b>Админ-панель</b>\n\nВыбери действие:",
        parse_mode="HTML",
        reply_markup=admin_menu_keyboard(),
    )
    try:
        await message.delete()
    except Exception:
        pass


@router.callback_query(F.data == "admin:menu")
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()
    await callback.message.edit_text(
        "🛠 <b>Админ-панель</b>\n\nВыбери действие:",
        parse_mode="HTML",
        reply_markup=admin_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin:noop")
async def admin_noop(callback: CallbackQuery):
    await callback.answer()


# =========================================================
# STATS
# =========================================================

@router.callback_query(F.data == "admin:stats")
async def admin_stats(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    async with async_session() as session:
        users_total = (await session.execute(
            select(func.count(User.id))
        )).scalar() or 0

        active_goals = (await session.execute(
            select(func.count(Goal.id)).where(Goal.status == "active")
        )).scalar() or 0

        completed_goals = (await session.execute(
            select(func.count(Goal.id)).where(Goal.status == "completed")
        )).scalar() or 0

        failed_goals = (await session.execute(
            select(func.count(Goal.id)).where(Goal.status == "failed")
        )).scalar() or 0

        active_challenges = (await session.execute(
            select(func.count(Challenge.id)).where(Challenge.status == "active")
        )).scalar() or 0

        total_kick = (await session.execute(
            select(func.coalesce(func.sum(User.balance), 0))
        )).scalar() or 0

        total_frozen = (await session.execute(
            select(func.coalesce(func.sum(User.frozen_kick), 0))
        )).scalar() or 0

        ach_total = (await session.execute(
            select(func.count(UserAchievement.id))
        )).scalar() or 0

    text = (
        "📊 <b>СТАТИСТИКА</b>\n\n"
        f"👥 Игроков: <b>{users_total}</b>\n\n"
        f"🎯 Активных целей: <b>{active_goals}</b>\n"
        f"🏆 Завершено целей: <b>{completed_goals}</b>\n"
        f"💀 Провалено целей: <b>{failed_goals}</b>\n\n"
        f"⚔️ Активных челленджей: <b>{active_challenges}</b>\n"
        f"🏅 Выдано достижений: <b>{ach_total}</b>\n\n"
        f"🪙 Всего KICK в обороте: <b>{total_kick}</b>\n"
        f"🔒 Всего заморожено: <b>{total_frozen}</b>"
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_back_keyboard(),
    )
    await callback.answer()


# =========================================================
# USERS LIST
# =========================================================

@router.callback_query(F.data.startswith("admin:users:"))
async def admin_users(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    page = int(callback.data.split(":")[2])

    async with async_session() as session:
        total = (await session.execute(
            select(func.count(User.id))
        )).scalar() or 0

        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

        result = await session.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset(page * PAGE_SIZE)
            .limit(PAGE_SIZE)
        )
        users = result.scalars().all()

    await callback.message.edit_text(
        f"👥 <b>Игроки</b> ({total})",
        parse_mode="HTML",
        reply_markup=admin_users_keyboard(users, page, total_pages),
    )
    await callback.answer()


# =========================================================
# USER CARD
# =========================================================

async def _render_user_card(
    bot,
    chat_id: int,
    message_id: int | None,
    user_id: int,
    edit: bool = True,
):
    """Общая функция отображения карточки юзера."""
    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            await bot.send_message(chat_id=chat_id, text="❌ Не найден.")
            return

        text = await _build_user_text(session, user)
        is_banned = bool(getattr(user, "is_banned", False))
        markup = admin_user_keyboard(user.id, is_banned)

    if edit and message_id is not None:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )
            return
        except Exception:
            pass

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup,
    )


@router.callback_query(F.data.startswith("admin:user:"))
async def admin_user(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    user_id = int(callback.data.split(":")[2])

    await _render_user_card(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        user_id=user_id,
        edit=True,
    )
    await callback.answer()


# =========================================================
# ADD / SUB KICK
# =========================================================

@router.callback_query(F.data.startswith("admin:addkick:"))
async def admin_addkick(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    _, _, uid_s, amount_s = callback.data.split(":")
    uid = int(uid_s)
    amount = int(amount_s)

    async with async_session() as session:
        user = await session.get(User, uid)
        if not user:
            await callback.answer("Не найден.", show_alert=True)
            return
        user.balance += amount
        await session.commit()

    await callback.answer(f"+{amount} KICK")
    await _render_user_card(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        user_id=uid,
        edit=True,
    )


@router.callback_query(F.data.startswith("admin:subkick:"))
async def admin_subkick(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    _, _, uid_s, amount_s = callback.data.split(":")
    uid = int(uid_s)
    amount = int(amount_s)

    async with async_session() as session:
        user = await session.get(User, uid)
        if not user:
            await callback.answer("Не найден.", show_alert=True)
            return
        user.balance = max(0, user.balance - amount)
        await session.commit()

    await callback.answer(f"−{amount} KICK")
    await _render_user_card(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        user_id=uid,
        edit=True,
    )


# =========================================================
# TOGGLE BAN
# =========================================================

@router.callback_query(F.data.startswith("admin:toggleban:"))
async def admin_toggleban(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    uid = int(callback.data.split(":")[2])

    async with async_session() as session:
        user = await session.get(User, uid)
        if not user:
            await callback.answer("Не найден.", show_alert=True)
            return

        if not hasattr(user, "is_banned"):
            await callback.answer(
                "Добавь поле is_banned в модель User.",
                show_alert=True,
            )
            return

        user.is_banned = not user.is_banned
        await session.commit()
        status = "Забанен" if user.is_banned else "Разбанен"

    await callback.answer(status)
    await _render_user_card(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        user_id=uid,
        edit=True,
    )


# =========================================================
# SEARCH
# =========================================================

@router.callback_query(F.data == "admin:search")
async def admin_search(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    await callback.message.edit_text(
        "🔎 Отправь telegram_id, @username или имя игрока.",
    )
    await state.set_state(AdminStates.waiting_for_user_query)
    await callback.answer()


@router.message(AdminStates.waiting_for_user_query)
async def admin_search_do(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return

    q = (message.text or "").strip()

    async with async_session() as session:
        if q.lstrip("-").isdigit():
            user = (await session.execute(
                select(User).where(User.telegram_id == int(q))
            )).scalar_one_or_none()
        else:
            user = (await session.execute(
                select(User).where(
                    (User.username == q.lstrip("@"))
                    | (User.first_name == q)
                )
            )).scalar_one_or_none()

    await state.clear()
    try:
        await message.delete()
    except Exception:
        pass

    if not user:
        await message.answer("❌ Не найден.")
        return

    # Отправляем карточку новым сообщением (без edit)
    await _render_user_card(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=None,
        user_id=user.id,
        edit=False,
    )


# =========================================================
# GRANT KICK
# =========================================================

@router.callback_query(F.data == "admin:grant")
async def admin_grant(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    await callback.message.edit_text(
        "🪙 Пришли: <code>telegram_id сумма</code>\n"
        "Например: <code>123456789 100</code>",
        parse_mode="HTML",
    )
    await state.set_state(AdminStates.waiting_for_grant)
    await callback.answer()


@router.message(AdminStates.waiting_for_grant)
async def admin_grant_do(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return

    try:
        tid_s, amount_s = (message.text or "").split()
        tid = int(tid_s)
        amount = int(amount_s)
    except Exception:
        await message.answer("❌ Формат: <id> <сумма>", parse_mode="HTML")
        return

    async with async_session() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == tid)
        )).scalar_one_or_none()
        if not user:
            await message.answer("❌ Игрок не найден.")
            return
        user.balance = max(0, user.balance + amount)
        await session.commit()

    await state.clear()
    await message.answer(f"✅ {amount:+d} KICK → {tid}")
    try:
        await message.delete()
    except Exception:
        pass


# =========================================================
# BAN
# =========================================================

@router.callback_query(F.data == "admin:ban")
async def admin_ban(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    await callback.message.edit_text(
        "🚫 Пришли telegram_id для бана/разбана.",
    )
    await state.set_state(AdminStates.waiting_for_ban)
    await callback.answer()


@router.message(AdminStates.waiting_for_ban)
async def admin_ban_do(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return

    try:
        tid = int((message.text or "").strip())
    except Exception:
        await message.answer("❌ Пришли число.")
        return

    async with async_session() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == tid)
        )).scalar_one_or_none()
        if not user:
            await message.answer("❌ Игрок не найден.")
            return
        if not hasattr(user, "is_banned"):
            await message.answer("❌ Добавь is_banned в User.")
            return
        user.is_banned = not user.is_banned
        await session.commit()
        status = "забанен" if user.is_banned else "разбанен"

    await state.clear()
    await message.answer(f"✅ {tid} — {status}")
    try:
        await message.delete()
    except Exception:
        pass


# =========================================================
# BROADCAST
# =========================================================

@router.callback_query(F.data == "admin:broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа.", show_alert=True)
        return

    await callback.message.edit_text(
        "📢 Пришли текст рассылки. Он уйдёт всем игрокам.",
    )
    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_for_broadcast)
async def admin_broadcast_do(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return

    text = message.text or ""
    if not text:
        return

    await state.clear()

    import asyncio

    async with async_session() as session:
        users = (await session.execute(select(User))).scalars().all()

    sent = 0
    failed = 0

    for u in users:
        try:
            await message.bot.send_message(
                chat_id=u.telegram_id,
                text=text,
                parse_mode="HTML",
            )
            sent += 1
        except Exception:
            failed += 1

        await asyncio.sleep(0.05)

    await message.answer(
        f"📢 Отправлено: {sent}\n❌ Ошибок: {failed}",
    )