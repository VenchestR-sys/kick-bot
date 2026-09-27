from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class GoalStep(Base):
    __tablename__ = "goal_steps"

    id: Mapped[int] = mapped_column(primary_key=True)

    goal_id: Mapped[int] = mapped_column(
        ForeignKey("goals.id"),
        index=True
    )

    day_number: Mapped[int] = mapped_column(Integer)

    title: Mapped[str] = mapped_column(String(500))

    # pending / completed / missed
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    # 📝 Что пользователь сделал в этот день
    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    available_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    goal = relationship("Goal", back_populates="steps")