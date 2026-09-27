import logging
import os

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


# =========================================================
# ПАПКИ (создаются ДО подключения к БД)
# =========================================================

os.makedirs("data", exist_ok=True)
os.makedirs("data/backup", exist_ok=True)
os.makedirs("logs", exist_ok=True)


DATABASE_URL = "sqlite+aiosqlite:///./data/kick.db"

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


log = logging.getLogger(__name__)


# =========================================================
# ПРОСТЫЕ МИГРАЦИИ
# =========================================================
# Формат: (таблица, колонка, SQL для добавления)
MIGRATIONS = [
    ("users", "bonus_channel_claimed",
     "ALTER TABLE users ADD COLUMN bonus_channel_claimed BOOLEAN DEFAULT 0"),
    ("users", "bonus_streak3_last_claim",
     "ALTER TABLE users ADD COLUMN bonus_streak3_last_claim DATETIME"),
    ("users", "bonus_streak5_last_claim",
     "ALTER TABLE users ADD COLUMN bonus_streak5_last_claim DATETIME"),
    ("users", "is_banned",
     "ALTER TABLE users ADD COLUMN is_banned BOOLEAN DEFAULT 0"),
    ("goals", "category",
     "ALTER TABLE goals ADD COLUMN category VARCHAR(30) DEFAULT 'other'"),
    ("goals", "description",
     "ALTER TABLE goals ADD COLUMN description TEXT"),
    ("goals", "result",
     "ALTER TABLE goals ADD COLUMN result TEXT"),
    ("goals", "missed_days_streak",
     "ALTER TABLE goals ADD COLUMN missed_days_streak INTEGER DEFAULT 0"),
    ("goals", "last_reminder_date",
     "ALTER TABLE goals ADD COLUMN last_reminder_date DATETIME"),
    ("goals", "warning_sent_at",
     "ALTER TABLE goals ADD COLUMN warning_sent_at DATETIME"),
    ("goal_steps", "note",
     "ALTER TABLE goal_steps ADD COLUMN note TEXT"),
    ("challenges", "category",
     "ALTER TABLE challenges ADD COLUMN category VARCHAR(30) DEFAULT 'other'"),
]


async def _run_migrations():
    """Проверяет, каких колонок нет, и добавляет их."""
    async with engine.begin() as conn:
        for table, column, sql in MIGRATIONS:
            # Проверяем, существует ли таблица
            result = await conn.execute(text(
                f"SELECT name FROM sqlite_master "
                f"WHERE type='table' AND name='{table}'"
            ))
            if result.scalar_one_or_none() is None:
                continue  # таблица ещё не создана

            # Проверяем, есть ли колонка
            result = await conn.execute(text(f"PRAGMA table_info({table})"))
            columns = {row[1] for row in result.fetchall()}

            if column in columns:
                continue

            try:
                await conn.execute(text(sql))
                log.info(f"✅ Миграция: {table}.{column}")
            except Exception as e:
                log.warning(f"⚠️  Не удалось добавить {table}.{column}: {e}")


async def init_db():
    from app.database.models.user import User
    from app.database.models.goal import Goal
    from app.database.models.goal_step import GoalStep
    from app.database.models.challenge import Challenge
    from app.database.models.achievement import UserAchievement
    from app.database.models.settings import UserSettings

    # Создаём таблицы (только новые)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Догоняем недостающие колонки
    await _run_migrations()