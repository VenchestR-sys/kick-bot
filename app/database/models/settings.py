from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    # 🔔 Уведомления
    goal_notifications: Mapped[bool] = mapped_column(default=True)
    challenge_notifications: Mapped[bool] = mapped_column(default=True)
    achievement_notifications: Mapped[bool] = mapped_column(default=True)

    # 🎯 Настройки целей
    show_goal_statistics: Mapped[bool] = mapped_column(default=True)

    # ⚔️ Настройки челленджей
    allow_challenge_invites: Mapped[bool] = mapped_column(default=True)