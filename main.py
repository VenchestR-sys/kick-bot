import asyncio
import logging

from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers import (
    start as start_router,
    goals as goals_router,
    challenges as challenges_router,
    profile as profile_router,
    rating as rating_router,
    settings as settings_router,
    help as help_router,
    admin as admin_router,
    bonus as bonus_router,
)
from app.bot.middlewares.menu_reset import MenuResetMiddleware
from app.bot.middlewares.ban import BanMiddleware
from app.services.goal_worker import (
    start_goal_worker,
    stop_goal_worker,
)
from app.database.database import init_db


# =========================================================
# НАСТРОЙКИ
# =========================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не задан. Создай файл .env с BOT_TOKEN=..."
    )


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger(__name__)


# =========================================================
# MAIN
# =========================================================

async def main():

    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # Middlewares
    dp.message.middleware(BanMiddleware())
    dp.callback_query.middleware(BanMiddleware())
    dp.message.middleware(MenuResetMiddleware())

    # Lifecycle
    dp.startup.register(start_goal_worker)
    dp.startup.register(challenges_router.start_challenge_worker)
    dp.shutdown.register(stop_goal_worker)
    dp.shutdown.register(challenges_router.stop_challenge_worker)

    # Routers
    dp.include_router(start_router.router)
    dp.include_router(help_router.router)
    dp.include_router(admin_router.router)
    dp.include_router(goals_router.router)
    dp.include_router(challenges_router.router)
    dp.include_router(profile_router.router)
    dp.include_router(rating_router.router)
    dp.include_router(settings_router.router)
    dp.include_router(bonus_router.router)
    await bot.delete_webhook(drop_pending_updates=True)

    log.info("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped")