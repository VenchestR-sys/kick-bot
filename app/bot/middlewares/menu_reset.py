from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.locales.texts import TEXTS


def _all_menu_texts() -> set[str]:
    keys = ("menu.my_goals", "menu.profile", "menu.rating",
            "menu.challenges", "menu.bonus", "menu.settings",
            "menu.help")
    result: set[str] = set()
    for lang in TEXTS:
        for k in keys:
            v = TEXTS[lang].get(k)
            if v:
                result.add(v)
    return result


_MENU_TEXTS = _all_menu_texts()


class MenuResetMiddleware(BaseMiddleware):
    """Если пользователь жмёт reply-кнопку главного меню — сбрасываем FSM."""

    async def __call__(self, handler, event, data):
        if isinstance(event, Message) and event.text in _MENU_TEXTS:
            state: FSMContext | None = data.get("state")
            if state is not None:
                try:
                    await state.clear()
                except Exception:
                    pass
        return await handler(event, data)