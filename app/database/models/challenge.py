from datetime import datetime

from sqlalchemy import (
    BigInteger, DateTime, ForeignKey, Integer, String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(primary_key=True)

    goal_id: Mapped[int] = mapped_column(
        ForeignKey("goals.id"),
        nullable=False
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    opponent_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # 🏷 Категория (дублируется от цели для быстрого фильтра)
    category: Mapped[str] = mapped_column(
        String(30),
        default="other"
    )

    duration_days: Mapped[int] = mapped_column(Integer)

    kick_stake: Mapped[int] = mapped_column(Integer)

    creator_progress: Mapped[int] = mapped_column(Integer, default=0)
    opponent_progress: Mapped[int] = mapped_column(Integer, default=0)

    creator_score: Mapped[int] = mapped_column(Integer, default=0)
    opponent_score: Mapped[int] = mapped_column(Integer, default=0)

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    creator_message_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    opponent_message_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )