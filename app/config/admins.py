# Список telegram_id админов. Заполни своими.
ADMIN_IDS: set[int] = {
    8369111955
}


def is_admin(telegram_id: int) -> bool:
    return telegram_id in ADMIN_IDS