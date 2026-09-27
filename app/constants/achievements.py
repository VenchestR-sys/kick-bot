ACHIEVEMENTS = {
    "first_step": {
        "emoji": "🌱",
        "ru": "Первый шаг",
        "en": "First step",
        "hy": "Առաջին քայլը",
        "hint_ru": "Выполни свой первый шаг",
        "hint_en": "Complete your first step",
        "hint_hy": "Կատարիր առաջին քայլը",
    },
    "streak_3": {
        "emoji": "🔥",
        "ru": "3 дня подряд",
        "en": "3 day streak",
        "hy": "3 օր անընդմեջ",
        "hint_ru": "Streak 3 дня",
        "hint_en": "3 day streak",
        "hint_hy": "3 օրվա streak",
    },
    "streak_7": {
        "emoji": "⚡",
        "ru": "Неделя силы",
        "en": "Week of power",
        "hy": "Ուժի շաբաթ",
        "hint_ru": "Streak 7 дней",
        "hint_en": "7 day streak",
        "hint_hy": "7 օրվա streak",
    },
    "streak_30": {
        "emoji": "💎",
        "ru": "Месяц дисциплины",
        "en": "Month of discipline",
        "hy": "Կարգապահության ամիս",
        "hint_ru": "Streak 30 дней",
        "hint_en": "30 day streak",
        "hint_hy": "30 օրվա streak",
    },
    "goal_complete_1": {
        "emoji": "🏆",
        "ru": "Первая вершина",
        "en": "First summit",
        "hy": "Առաջին գագաթը",
        "hint_ru": "Заверши первую цель",
        "hint_en": "Complete your first goal",
        "hint_hy": "Ավարտիր առաջին նպատակը",
    },
    "goal_complete_5": {
        "emoji": "👑",
        "ru": "Покоритель",
        "en": "Conqueror",
        "hy": "Նվաճող",
        "hint_ru": "Заверши 5 целей",
        "hint_en": "Complete 5 goals",
        "hint_hy": "Ավարտիր 5 նպատակ",
    },
    "challenge_win_1": {
        "emoji": "⚔️",
        "ru": "Дуэлянт",
        "en": "Duelist",
        "hy": "Մենամարտիկ",
        "hint_ru": "Выиграй первый челлендж",
        "hint_en": "Win your first challenge",
        "hint_hy": "Հաղթիր առաջին չելենջը",
    },
    "challenge_win_5": {
        "emoji": "🗡",
        "ru": "Гладиатор",
        "en": "Gladiator",
        "hy": "Գլադիատոր",
        "hint_ru": "Выиграй 5 челленджей",
        "hint_en": "Win 5 challenges",
        "hint_hy": "Հաղթիր 5 չելենջ",
    },
    "level_5": {
        "emoji": "⭐",
        "ru": "Уровень 5",
        "en": "Level 5",
        "hy": "Մակարդակ 5",
        "hint_ru": "Достигни 5 уровня",
        "hint_en": "Reach level 5",
        "hint_hy": "Հասիր 5-րդ մակարդակին",
    },
    "level_10": {
        "emoji": "🌟",
        "ru": "Уровень 10",
        "en": "Level 10",
        "hy": "Մակարդակ 10",
        "hint_ru": "Достигни 10 уровня",
        "hint_en": "Reach level 10",
        "hint_hy": "Հասիր 10-րդ մակարդակին",
    },
    "night_owl": {
        "emoji": "🦉",
        "ru": "Полуночник",
        "en": "Night owl",
        "hy": "Գիշերային թռչուն",
        "hint_ru": "Выполни шаг после 22:00",
        "hint_en": "Complete a step after 10 PM",
        "hint_hy": "Կատարիր քայլը 22:00-ից հետո",
    },
}


def achievement_name(code: str, language: str = "ru") -> str:
    a = ACHIEVEMENTS.get(code)
    if not a:
        return code
    return f"{a['emoji']} {a.get(language) or a['ru']}"


def achievement_hint(code: str, language: str = "ru") -> str:
    a = ACHIEVEMENTS.get(code)
    if not a:
        return ""
    return a.get(f"hint_{language}") or a.get("hint_ru") or ""