from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message


async def safe_edit(message: Message, text: str, reply_markup=None):
    """
    Универсальное редактирование сообщения.

    - Если у сообщения есть text — edit_text
    - Если у сообщения есть caption (фото) — edit_caption
    - Иначе — ничего не делаем

    Ошибки TelegramBadRequest проглатываются, чтобы не ронять хендлер.
    """
    try:
        if message.text is not None:
            await message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
        elif message.caption is not None:
            await message.edit_caption(
                caption=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
    except TelegramBadRequest:
        # "message is not modified" или другие ошибки — просто игнорируем
        pass