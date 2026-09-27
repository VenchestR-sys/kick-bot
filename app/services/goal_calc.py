"""
Общие функции расчёта наград и стоимости создания цели.
Используются в:
  - app.bot.routers.goals
  - app.services.goal_worker
"""


def calculate_rewards(duration: int) -> tuple[str, int, int]:
    """
    Возвращает (difficulty, score_reward, kick_reward).
    """
    if duration <= 3:
        return "hard", 30, 10
    if duration <= 14:
        return "normal", 70, 20
    return "hard", 150, 50


def calculate_creation_cost(duration: int) -> int:
    """
    Сколько KICK замораживается при создании цели.
    """
    if duration <= 3:
        return 5
    if duration <= 14:
        return 10
    if duration <= 30:
        return 20
    if duration <= 90:
        return 30
    return 50


def calculate_level(xp: int) -> int:
    return max(1, xp // 100 + 1)