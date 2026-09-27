from datetime import datetime

from sqlalchemy import (
    DateTime, ForeignKey, String, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    # Код ачивки из app/constants/achievements.py
    code: Mapped[str] = mapped_column(String(50), index=True)

    unlocked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint("user_id", "code", name="uq_user_achievement"),
    )

    user = relationship("User", back_populates="achievements")