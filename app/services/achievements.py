from sqlalchemy import select, func

from app.constants.achievements import ACHIEVEMENTS
from app.database.models.achievement import UserAchievement
from app.database.models.goal import Goal
from app.database.models.user import User


async def _has(session, user_id: int, code: str) -> bool:
    result = await session.execute(
        select(UserAchievement.id).where(
            UserAchievement.user_id == user_id,
            UserAchievement.code == code,
        )
    )
    return result.scalar_one_or_none() is not None


async def grant(session, user_id: int, code: str) -> bool:
    """Выдаёт ачивку, если её нет. True — если только что выдали."""
    if code not in ACHIEVEMENTS:
        return False
    if await _has(session, user_id, code):
        return False

    session.add(UserAchievement(user_id=user_id, code=code))
    return True


async def check_and_grant(session, user: User) -> list[str]:
    """Проверяет все ачивки пользователя, выдаёт недостающие."""
    granted: list[str] = []

    # --- streak ---
    if user.current_streak >= 3 and await grant(session, user.id, "streak_3"):
        granted.append("streak_3")
    if user.current_streak >= 7 and await grant(session, user.id, "streak_7"):
        granted.append("streak_7")
    if user.current_streak >= 30 and await grant(session, user.id, "streak_30"):
        granted.append("streak_30")

    # --- уровень ---
    if user.level >= 5 and await grant(session, user.id, "level_5"):
        granted.append("level_5")
    if user.level >= 10 and await grant(session, user.id, "level_10"):
        granted.append("level_10")

    # --- завершённые цели ---
    done = (await session.execute(
        select(func.count(Goal.id)).where(
            Goal.user_id == user.id,
            Goal.status == "completed",
        )
    )).scalar() or 0

    if done >= 1 and await grant(session, user.id, "goal_complete_1"):
        granted.append("goal_complete_1")
    if done >= 5 and await grant(session, user.id, "goal_complete_5"):
        granted.append("goal_complete_5")

    # --- выигранные челленджи ---
    from app.database.models.challenge import Challenge
    wins = (await session.execute(
        select(func.count(Challenge.id)).where(
            Challenge.winner_id == user.id,
        )
    )).scalar() or 0

    if wins >= 1 and await grant(session, user.id, "challenge_win_1"):
        granted.append("challenge_win_1")
    if wins >= 5 and await grant(session, user.id, "challenge_win_5"):
        granted.append("challenge_win_5")

    return granted


async def grant_first_step(session, user_id: int) -> bool:
    return await grant(session, user_id, "first_step")


async def grant_night_owl(session, user_id: int) -> bool:
    return await grant(session, user_id, "night_owl")


async def get_user_achievements(session, user_id: int) -> set[str]:
    result = await session.execute(
        select(UserAchievement.code).where(
            UserAchievement.user_id == user_id,
        )
    )
    return set(result.scalars().all())