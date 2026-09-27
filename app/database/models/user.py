from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False
    )

    username: Mapped[str | None]
    first_name: Mapped[str | None]

    # Доступные KICK
    balance: Mapped[int] = mapped_column(default=100)
    frozen_kick: Mapped[int] = mapped_column(default=0)

    score: Mapped[int] = mapped_column(default=0)
    xp: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=1)

    current_streak: Mapped[int] = mapped_column(default=0)
    best_streak: Mapped[int] = mapped_column(default=0)

    last_activity_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    last_bot_message_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    language: Mapped[str] = mapped_column(default="ru")

    # 🔔 Настройки уведомлений
    goal_notifications: Mapped[bool] = mapped_column(default=True)
    challenge_notifications: Mapped[bool] = mapped_column(default=True)
    achievement_notifications: Mapped[bool] = mapped_column(default=True)

    # 🚫 Бан
    is_banned: Mapped[bool] = mapped_column(default=False)

    # 🎁 Бонусы
    bonus_channel_claimed: Mapped[bool] = mapped_column(default=False)
    bonus_streak3_last_claim: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    bonus_streak5_last_claim: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    # Связи
    goals = relationship(
        "Goal",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    achievements = relationship(
        "UserAchievement",
        back_populates="user",
        cascade="all, delete-orphan"
    )