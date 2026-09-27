"""
Держит reply-клавиатуру главного меню видимой.

Работает через monkey-patch ScreenManager.show: перед каждым показом
экрана проверяем, что в чате установлено главное меню нужного языка.
Если языка нет / он сменился — пересоздаём ОДНО анкерное сообщение.

Подключается автоматически при импорте.
"""

from app.bot.keyboards.main import main_menu
from app.bot.utils.screens import ScreenManager


# chat_id -> (message_id анкера, язык анкера)
_anchors: dict[int, tuple[int, str]] = {}

_installed = False
_original_show = None


_ANCHOR_TEXT = "\u2063"


async def _ensure_anchor(bot, chat_id: int, language: str) -> None:
    """
    Гарантирует, что в чате есть ровно ОДНО анкерное сообщение
    с reply-клавиатурой главного меню на нужном языке.
    """
    current = _anchors.get(chat_id)

    # Уже есть анкер на этом языке — ничего не делаем
    if current is not None and current[1] == language:
        return

    # Если был старый анкер — удаляем его
    if current is not None:
        old_message_id, _ = current
        try:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=old_message_id,
            )
        except Exception:
            pass

    # Отправляем новый анкер
    try:
        sent = await bot.send_message(
            chat_id=chat_id,
            text=_ANCHOR_TEXT,
            reply_markup=main_menu(language),
            disable_notification=True,
        )
        _anchors[chat_id] = (sent.message_id, language)

    except Exception:
        # не смогли отправить — не страшно, попробуем в следующий раз
        pass


async def _patched_show(
    bot,
    user,
    chat_id: int,
    session,
    text: str,
    reply_markup=None,
    **kwargs,
):
    """Обёртка над ScreenManager.show — сначала прикрепляет главное меню."""
    language = getattr(user, "language", None) or "ru"

    await _ensure_anchor(bot, chat_id, language)

    return await _original_show(
        bot=bot,
        user=user,
        chat_id=chat_id,
        session=session,
        text=text,
        reply_markup=reply_markup,
        **kwargs,
    )


def install() -> None:
    """Однократно патчит ScreenManager.show."""
    global _installed, _original_show

    if _installed:
        return

    _original_show = ScreenManager.show
    ScreenManager.show = _patched_show
    _installed = True
    

install()