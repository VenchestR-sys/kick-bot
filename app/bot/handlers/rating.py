from pathlib import Path

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy import select

from app.bot.keyboards.rating import rating_keyboard
from app.bot.utils.safe_edit import safe_edit
from app.bot.utils.screens import ScreenManager
from app.database.database import async_session
from app.database.models.user import User
from app.locales.texts import t


router = Router()


# ============================================================
# MEDIA
# ============================================================

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
RATING_IMAGE_RU = MEDIA_DIR / "rating_ru.png"


# ============================================================
# HELPERS
# ============================================================

def _name(u: User, lang: str) -> str:
    return u.first_name or u.username or t(lang, "common.player")


def _value(u: User, rt: str) -> int:
    if rt == "streak":
        return u.current_streak
    if rt == "xp":
        return u.xp
    return u.score


def _icon(rt: str) -> str:
    return {"streak": "🔥", "xp": "⚡"}.get(rt, "⭐")


def _metric_name(rt: str, lang: str) -> str:
    return (
        t(lang, f"rating.metric_{rt}")
        if rt in ("streak", "xp", "score")
        else t(lang, "rating.metric_score")
    )


def _order(rt: str):
    if rt == "streak":
        return (User.current_streak.desc(), User.xp.desc(), User.id.asc())
    if rt == "xp":
        return (User.xp.desc(), User.score.desc(), User.id.asc())
    return (User.score.desc(), User.xp.desc(), User.id.asc())


def _fmt(v: int, rt: str, lang: str) -> str:
    if rt == "streak":
        return f"{v} {t(lang, 'rating.days_short')}"
    if rt == "xp":
        return f"{v} XP"
    return f"{v} SCORE"


async def build_rating(session, user: User, rt: str):
    lang = user.language or "ru"

    result = await session.execute(select(User).order_by(*_order(rt)))
    users = result.scalars().all()

    top = users[:10]
    cur_val = _value(user, rt)

    above = [u for u in users if _value(u, rt) > cur_val]
    place = len(above) + 1

    next_player = None
    if above:
        next_player = sorted(above, key=lambda u: _value(u, rt))[0]

    icon = _icon(rt)

    text = f"{t(lang, 'rating.title')}\n\n━━━━━━━━━━━━━━━━━━━━\n\n"

    if top:
        text += f"{t(lang, 'rating.top_players')}\n\n"
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}

        for i, p in enumerate(top[:3], start=1):
            nm = _name(p, lang)
            v = _value(p, rt)
            medal = medals[i]
            if p.id == user.id:
                text += (
                    f"{medal} <b>{nm}</b> 👈\n"
                    f"{icon} <b>{_fmt(v, rt, lang)}</b>\n"
                    f"🏆 LVL {p.level}\n\n"
                )
            else:
                text += (
                    f"{medal} <b>{nm}</b>\n"
                    f"{icon} <b>{_fmt(v, rt, lang)}</b>\n"
                    f"🏆 LVL {p.level}\n\n"
                )

    if len(top) > 3:
        text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, p in enumerate(top[3:], start=4):
            nm = _name(p, lang)
            v = _value(p, rt)
            if p.id == user.id:
                text += f"👉 <b>#{i} {nm}</b>\n   {icon} <b>{_fmt(v, rt, lang)}</b>\n\n"
            else:
                text += f"<b>#{i}</b> {nm}\n   {icon} {_fmt(v, rt, lang)}\n\n"

    text += (
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t(lang, 'rating.your_result')}\n\n"
        f"{t(lang, 'rating.place')}: <b>#{place}</b>\n"
        f"{icon} <b>{_fmt(cur_val, rt, lang)}</b>\n"
        f"{t(lang, 'rating.level')}: <b>{user.level}</b>\n"
        f"{t(lang, 'rating.streak_label')}: <b>{user.current_streak} {t(lang, 'rating.days_short')}</b>\n"
    )

    if next_player:
        nv = _value(next_player, rt)
        diff = nv - cur_val
        nn = _name(next_player, lang)
        text += (
            f"\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t(lang, 'rating.next_opponent')}\n\n"
            f"⬆️ #{place - 1} <b>{nn}</b>\n"
            f"{icon} <b>{_fmt(nv, rt, lang)}</b>\n\n"
            f"{t(lang, 'rating.to_him')}: <b>{diff}</b> {_metric_name(rt, lang)}\n"
        )
    else:
        text += f"\n━━━━━━━━━━━━━━━━━━━━\n\n{t(lang, 'rating.at_top')}\n"

    if place > 10:
        tenth = top[-1] if top else None
        if tenth:
            tv = _value(tenth, rt)
            diff = max(0, tv - cur_val)
            pct = int(cur_val / max(tv, 1) * 100)
            pct = min(pct, 100)
            filled = int(pct / 100 * 10)
            bar = "🟩" * filled + "⬜" * (10 - filled)
            text += (
                f"\n━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{t(lang, 'rating.path_top10')}\n\n"
                f"{bar}\n\n"
                f"{t(lang, 'rating.to_top10')}: <b>{diff}</b> {_metric_name(rt, lang)}\n\n"
                f"{t(lang, 'rating.keep_going')}"
            )
    else:
        text += (
            f"\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t(lang, 'rating.you_in_top10')}\n\n"
            f"{t(lang, 'rating.you_in_top10_hint')}"
        )

    return text


# ============================================================
# SHOW RATING (с фото для всех языков)
# ============================================================

async def show_rating(
    bot,
    chat_id: int,
    telegram_id: int,
    rating_type: str,
    edit: bool = False,
    edit_message=None,
    user=None,
    session=None,
):
    """
    Показывает рейтинг.

    Если edit=True и edit_message передан — редактирует существующее сообщение.
    Иначе — удаляет предыдущий экран и отправляет новое (с фото, если есть).
    """

    close_session = False
    if session is None:
        session = async_session()
        await session.__aenter__()
        close_session = True

    try:
        if user is None:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return

        lang = user.language or "ru"
        text = await build_rating(session, user, rating_type)
        markup = rating_keyboard(lang, rating_type)

        # ---- Редактирование существующего сообщения ----
        if edit and edit_message is not None:
            await safe_edit(edit_message, text, reply_markup=markup)
            return

        # ---- Отправка нового (удаляем предыдущий экран) ----
        await ScreenManager.clear_previous(
            bot=bot,
            user=user,
            chat_id=chat_id,
            session=session,
        )

        new_message = None

        if RATING_IMAGE_RU.exists():

            if len(text) <= 1024:
                caption = text
            else:
                # короткая подпись, если не влезает в caption
                icon = _icon(rating_type)
                caption = (
                    f"{t(lang, 'rating.title')}\n\n"
                    f"🏆 LVL: <b>{user.level}</b>\n"
                    f"{icon} {_metric_name(rating_type, lang)}: "
                    f"<b>{_fmt(_value(user, rating_type), rating_type, lang)}</b>\n\n"
                    f"👇"
                )

            try:
                new_message = await bot.send_photo(
                    chat_id=chat_id,
                    photo=FSInputFile(RATING_IMAGE_RU),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
            except Exception:
                new_message = None

        if new_message is None:
            new_message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )

        user.last_bot_message_id = new_message.message_id
        await session.commit()

    finally:
        if close_session:
            await session.__aexit__(None, None, None)


# ============================================================
# HANDLERS
# ============================================================

@router.message(
    F.text.in_([
        "🏆 Рейтинг",
        "🏆 Rating",
        "🏆 Վարկանիշ",
    ])
)
async def rating_handler(message: Message):
    await show_rating(
        bot=message.bot,
        chat_id=message.chat.id,
        telegram_id=message.from_user.id,
        rating_type="score",
        edit=False,
    )
    await message.delete()


@router.callback_query(F.data == "rating:score")
async def rating_score_handler(callback: CallbackQuery):
    await show_rating(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        telegram_id=callback.from_user.id,
        rating_type="score",
        edit=True,
        edit_message=callback.message,
    )
    await callback.answer()


@router.callback_query(F.data == "rating:streak")
async def rating_streak_handler(callback: CallbackQuery):
    await show_rating(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        telegram_id=callback.from_user.id,
        rating_type="streak",
        edit=True,
        edit_message=callback.message,
    )
    await callback.answer()


@router.callback_query(F.data == "rating:xp")
async def rating_xp_handler(callback: CallbackQuery):
    await show_rating(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        telegram_id=callback.from_user.id,
        rating_type="xp",
        edit=True,
        edit_message=callback.message,
    )
    await callback.answer()