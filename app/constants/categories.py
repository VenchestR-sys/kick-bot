CATEGORIES = {
    "sport": {
        "emoji": "💪",
        "ru": "Спорт",
        "en": "Sport",
        "hy": "Սպորտ",
    },
    "study": {
        "emoji": "📚",
        "ru": "Учёба",
        "en": "Study",
        "hy": "Ուսում",
    },
    "work": {
        "emoji": "💼",
        "ru": "Работа",
        "en": "Work",
        "hy": "Աշխատանք",
    },
    "health": {
        "emoji": "🧘",
        "ru": "Здоровье",
        "en": "Health",
        "hy": "Առողջություն",
    },
    "creative": {
        "emoji": "🎨",
        "ru": "Творчество",
        "en": "Creative",
        "hy": "Ստեղծագործություն",
    },
    "other": {
        "emoji": "🎯",
        "ru": "Другое",
        "en": "Other",
        "hy": "Այլ",
    },
}


def category_name(code: str, language: str = "ru") -> str:
    cat = CATEGORIES.get(code) or CATEGORIES["other"]
    return f"{cat['emoji']} {cat.get(language) or cat['ru']}"