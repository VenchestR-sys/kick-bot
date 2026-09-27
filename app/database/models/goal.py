from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    title: Mapped[str] = mapped_column(String(500))

    # 📝 Описание цели (зачем она нужна)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 🏷 Категория (sport / study / work / health / creative / other)
    category: Mapped[str] = mapped_column(String(30), default="other")

    duration_days: Mapped[int] = mapped_column(Integer)

    difficulty: Mapped[str] = mapped_column(String(50), default="normal")

    score_reward: Mapped[int] = mapped_column(Integer, default=0)
    kick_reward: Mapped[int] = mapped_column(Integer, default=0)

    start_date: Mapped[datetime] = mapped_column(DateTime)
    deadline: Mapped[datetime] = mapped_column(DateTime)

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        index=True
    )

    # --- контроль пропусков ---
    missed_days_streak: Mapped[int] = mapped_column(Integer, default=0)

    last_reminder_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    warning_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # 🎯 Чего именно хочет достичь пользователь
    result: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="goals")

    steps = relationship(
        "GoalStep",
        back_populates="goal",
        cascade="all, delete-orphan"
    )