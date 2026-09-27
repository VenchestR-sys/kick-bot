TEXTS = {

    # ========================================================
    # РУССКИЙ
    # ========================================================
    "ru": {
        # ---------------- HELP ----------------
        "menu.help": "❓ Помощь",
                # ---------- МЕНЮ: БОНУС ----------
        "menu.bonus": "🎁 Бонус",

        # ---------- БОНУС ----------
        "bonus.title": "🎁 <b>БОНУСЫ</b>",
        "bonus.subtitle": (
            "Выполняй задания и получай KICK бесплатно!\n\n"
            "Выбери задание 👇"
        ),

        "bonus.channel_title": "📢 <b>ПОДПИСКА НА КАНАЛ</b>",
        "bonus.channel_body": (
            "Подпишись на наш канал и получи "
            "<b>+50 KICK</b> на счёт.\n\n"
            "После подписки нажми «✅ Проверить».\n\n"
            "🔗 <a href=\"https://t.me/kickgame_official\">kickgame_official</a>"
        ),
        "bonus.channel_button": "✅ Проверить",
        "bonus.channel_button_go": "📢 Подписаться",
        "bonus.channel_claimed": (
            "✅ Ты уже получил награду за подписку.\n\n"
            "Возвращайся за другими бонусами!"
        ),
        "bonus.channel_success": (
            "🎉 <b>+50 KICK</b>\n\n"
            "Спасибо за подписку! Награда зачислена."
        ),
        "bonus.channel_not_subscribed": (
            "⚠️ Ты ещё не подписан на канал.\n\n"
            "Подпишись и нажми «Проверить» снова."
        ),
        "bonus.channel_check_error": (
            "❌ Не удалось проверить подписку. Попробуй позже."
        ),

        "bonus.streak3_title": "🔥 <b>3 ДНЯ ПОДРЯД</b>",
        "bonus.streak3_body": (
            "Выполни любое задание 3 дня подряд и получи "
            "<b>+10 KICK</b>.\n\n"
            "Можно получать раз в неделю."
        ),
        "bonus.streak5_title": "⚡ <b>5 ДНЕЙ ПОДРЯД</b>",
        "bonus.streak5_body": (
            "Выполни любое задание 5 дней подряд и получи "
            "<b>+30 KICK</b>.\n\n"
            "Можно получать раз в неделю."
        ),

        "bonus.claim_button": "🎁 Забрать",
        "bonus.claimed_today": "✅ Уже получено. Возвращайся позже.",
        "bonus.not_enough_streak": (
            "⚠️ Ты пока не выполнил условие.\n\n"
            "Твой streak: <b>{streak}</b>"
        ),
        "bonus.claim_success": (
            "🎉 <b>+{amount} KICK</b>\n\n"
            "Награда зачислена!"
        ),
        "bonus.week_wait": (
            "⏳ Следующая награда будет доступна позже."
        ),

        "bonus.back": "🔙 К бонусам",    
        "help.title": "❓ <b>КАК ИГРАТЬ В KICK</b>",
        "help.body": (
            "⚡ <b>KICK</b> — игра, где твои цели превращаются в соревнование.\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🎯 <b>ЦЕЛИ</b>\n"
            "• Создай цель и выбери срок\n"
            "• Каждый день отмечай шаг\n"
            "• 2 пропуска подряд — цель провалена, KICK сгорают\n\n"
            "🪙 <b>KICK</b>\n"
            "• Стартовый баланс — 100 KICK\n"
            "• При создании цели часть KICK замораживается\n"
            "• Выполнил цель — KICK возвращаются + награда\n"
            "• Провалил — KICK не возвращаются\n\n"
            "⚔️ <b>ЧЕЛЛЕНДЖИ</b>\n"
            "• Брось вызов другому игроку\n"
            "• Оба вносят ставку, победитель забирает банк\n\n"
            "🔥 <b>STREAK</b>\n"
            "• Отмечай шаги каждый день\n"
            "• Streak растёт — ты получаешь больше наград\n\n"
            "🏆 <b>ДОСТИЖЕНИЯ</b>\n"
            "• Открываются за прогресс, streak и победы\n"
            "• Смотри их в профиле\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🔥 Не сдавайся — KICK ждёт!"
        ),
        "help.commands": (
            "⚙️ <b>Команды</b>\n\n"
            "/start — главное меню\n"
            "/help — эта справка\n"
            "/cancel — отменить текущее действие"
        ),
        "help.cancelled": "✅ Действие отменено.",

        # ---------------- КНОПКИ ----------------
        "btn.duration.1": "1 день",
        "btn.duration.3": "3 дня",
        "btn.duration.7": "7 дней",
        "btn.duration.14": "14 дней",
        "btn.duration.30": "30 дней",
        "btn.duration.90": "90 дней",
        "btn.duration.custom": "✏️ Свой срок",

        "btn.start": "🚀 Начать",
        "btn.edit": "✏️ Редактировать",
        "btn.cancel": "❌ Отменить",

        "btn.edit_title": "🎯 Название",
        "btn.edit_category": "🏷 Категория",
        "btn.edit_description": "📝 Зачем мне это",
        "btn.edit_result": "🎯 Чего хочу достичь",
        "btn.edit_duration": "⏱ Срок",

        "btn.skip": "⏭ Пропустить",
        "btn.back": "🔙 Назад",
        "btn.back_to_goal": "🔙 К цели",
        "btn.back_to_goals": "🔙 К списку целей",
        "btn.back_to_challenges": "🔙 К челленджам",
        "btn.back_to_challenge": "🔙 К челленджу",

        "btn.create_goal": "➕ Создать цель",
        "btn.find_opponent": "⚔️ Найти соперника",
        "btn.complete_today": "✅ Выполнить сегодняшний шаг",
        "btn.complete_today_short": "✅ Выполнить сегодня",
        "btn.heatmap": "📅 Полоса прогресса",
        "btn.all_steps": "📋 Все шаги",
        "btn.cancel_goal": "🗑 Отменить цель",
        "btn.yes_cancel": "🗑 Да, отменить",
        "btn.no_back": "🔙 Нет, вернуться",

        "btn.throw_challenge": "⚔️ Кинуть вызов",
        "btn.choose_other": "🔙 Выбрать другого",
        "btn.accept": "⚔️ Принять вызов",
        "btn.decline": "❌ Отклонить",
        "btn.open_challenge": "⚔️ Открыть челлендж",
        "btn.refresh": "🔄 Обновить",
        "btn.create_challenge": "⚔️ Создать челлендж",
        "btn.history": "📜 История челленджей",
        "btn.filter_all": "🔷 Все категории",

        # ---------------- КАТЕГОРИИ ----------------
        "category.title": "🏷 <b>ВЫБЕРИ КАТЕГОРИЮ</b>",
        "category.hint": "К какой сфере относится твоя цель?",

        # ---------- ГЛАВНОЕ МЕНЮ ----------
        "menu.my_goals": "🎯 Мои цели",
        "menu.profile": "👤 Профиль",
        "menu.rating": "🏆 Рейтинг",
        "menu.challenges": "⚔️ Челленджи",
        "menu.ai_coach": "🤖 AI Coach",
        "menu.settings": "⚙️ Настройки",

        # ---------- ОБЩИЕ ----------
        "common.back": "🔙 Назад",
        "common.cancel": "❌ Отмена",
        "common.yes": "✅ Да",
        "common.no": "❌ Нет",
        "common.user_not_found": "Пользователь не найден.",
        "common.goal_not_found": "Цель не найдена.",
        "common.player": "Игрок",
        "common.days": "дней",
        "common.hours_short": "ч.",
        "common.minutes_short": "мин.",

        # ---------- ЦЕЛИ ----------
        "goals.title": "🎯 <b>МОИ ЦЕЛИ</b>",
        "goals.no_goals": (
            "У тебя пока нет активных целей.\n\n"
            "Создай первую цель и начни двигаться вперёд! 🚀"
        ),
        "goals.choose": "Выбери цель:",

        "goals.new": "🎯 <b>НОВАЯ ЦЕЛЬ</b>",
        "goals.choose_duration": (
            "Сначала выбери срок цели.\n\n"
            "Чем дольше цель — тем выше потенциальная награда.\n\n"
            "💡 После создания часть KICK будет заморожена."
        ),
        "goals.custom_duration": "⏱ <b>СВОЙ СРОК</b>",
        "goals.enter_days": "Введи количество дней.\n\nНапример:\n<code>45</code>",
        "goals.enter_days_number": "Введи количество дней числом.",
        "goals.min_duration": "Срок должен быть минимум 1 день.",
        "goals.max_duration": "Максимальный срок — 365 дней.",
        "goals.enter_title": (
            "🎯 <b>НАЗВАНИЕ ЦЕЛИ</b>\n\n"
            "Напиши, чего ты хочешь достичь.\n\n"
            "Например:\n"
            "<i>Выучить Python</i>\n"
            "<i>Тренироваться каждый день</i>\n"
            "<i>Прочитать 5 книг</i>"
        ),
        "goals.title_empty": "Название цели не может быть пустым.",
        "goals.title_too_long": "Название цели слишком длинное.",

        "goals.duration_label": "⏱ Срок",
        "goals.difficulty_label": "🔥 Сложность",
        "goals.difficulty_hard": "сложная",
        "goals.difficulty_normal": "обычная",
        "goals.preview": "🚀 <b>ПРЕДПРОСМОТР ЦЕЛИ</b>",
        "goals.conditions": "💰 <b>УСЛОВИЯ</b>",
        "goals.freeze": "🔒 Заморозка",
        "goals.reward": "🪙 Награда",
        "goals.balance": "🪙 Твой баланс",
        "goals.cancel_72": "После начала цели отменить её можно только в течение 72 часов.",

        "goals.enter_description": (
            "📝 <b>ОПИСАНИЕ ЦЕЛИ</b>\n\n"
            "Опиши коротко, зачем тебе это.\n\n"
            "Например:\n"
            "<i>Хочу стать backend-разработчиком к лету</i>\n\n"
            "Или нажми «Пропустить»."
        ),
        "goals.description_label": "📝 Описание",
        "goals.new_description": "✏️ <b>НОВОЕ ОПИСАНИЕ</b>",
        "goals.enter_new_description": "Напиши новое описание.",
        "goals.edit_description": "📝 Описание",

        "goals.enter_result": (
            "🎯 <b>КАКОЙ РЕЗУЛЬТАТ ХОЧЕШЬ ПОЛУЧИТЬ?</b>\n\n"
            "Опиши коротко и конкретно, что должно "
            "получиться в конце.\n\n"
            "Например:\n"
            "<i>Пробежать 10 км без остановки</i>\n"
            "<i>Сдать IELTS на 7.0</i>\n"
            "<i>Написать 30 000 слов романа</i>\n\n"
            "Или нажми «Пропустить»."
        ),
        "goals.result_label": "🎯 Результат",
        "goals.new_result": "✏️ <b>НОВЫЙ РЕЗУЛЬТАТ</b>",
        "goals.enter_new_result": "Опиши новый результат.",
        "goals.edit_result": "🎯 Результат",

        "goals.editing": "✏️ <b>РЕДАКТИРОВАНИЕ</b>",
        "goals.what_edit": "Что хочешь изменить?",
        "goals.new_title": "✏️ <b>НОВОЕ НАЗВАНИЕ</b>",
        "goals.enter_new_title": "Напиши новое название цели.",
        "goals.new_duration": "⏱ <b>НОВЫЙ СРОК</b>",
        "goals.choose_new_duration": "Выбери новый срок:",

        "goals.started": "🚀 <b>ЦЕЛЬ НАЧАТА!</b>",
        "goals.first_step_wait": "🔥 Первый шаг уже ждёт тебя!",
        "goals.remember_cancel": "Помни: отменить цель можно только в течение первых 72 часов.",

        "goals.insufficient_kick": "❌ <b>Недостаточно KICK</b>",
        "goals.need_kick": "Для этой цели необходимо",
        "goals.data_lost": "Данные цели потеряны.",
        "goals.creation_cancelled": "❌ <b>Создание цели отменено.</b>",
        "goals.can_create_again": "Ты можешь создать новую цель в любое время.",
        "goals.active_not_found": "Активная цель не найдена.",

        "goals.status_active": "🟢 Активна",
        "goals.status_completed": "🏆 Завершена",
        "goals.status_cancelled": "❌ Отменена",
        "goals.status_failed": "💀 Провалена",

        "goals.progress": "📈 Прогресс",
        "goals.completed": "✅ Выполнено",
        "goals.frozen": "🔒 Заморожено",
        "goals.cancel_available": "🗑 Отмена доступна ещё",
        "goals.cancel_unavailable": "🔒 <b>Отмена недоступна</b>",

        "goals.step_not_found": "Сегодняшний шаг не найден.",
        "goals.step_already_done": "Сегодняшний шаг уже выполнен! ✅",
        "goals.first_step_unavailable": "⏳ Первый шаг пока недоступен.\n\nПопробуй через",

        "goals.completed_title": "🏆 <b>ЦЕЛЬ ЗАВЕРШЕНА!</b>",
        "goals.all_steps_done": "🔥 Все шаги выполнены!",
        "goals.step_reward": "🪙 Награда",
        "goals.xp": "⚡ XP",
        "goals.step_completed": "✅ <b>ШАГ ВЫПОЛНЕН!</b>",
        "goals.day": "📅 День",
        "goals.level_up": "🎉 <b>LEVEL UP!</b>",
        "goals.new_level": "🏆 Новый уровень",

        "goals.steps": "📋 <b>ШАГИ ЦЕЛИ</b>",
        "goals.day_word": "День",

        "goals.cancel_confirm": "🗑 <b>ОТМЕНИТЬ ЦЕЛЬ?</b>",
        "goals.returned": "🔒 Вернётся",
        "goals.cancel_info": "Цель будет отменена и больше не будет считаться активной.",
        "goals.cancel_unavailable_title": "🔒 <b>ОТМЕНА НЕДОСТУПНА</b>",
        "goals.cancel_72_passed": (
            "72 часа после создания цели уже прошли.\n\n"
            "Теперь цель можно только продолжать."
        ),
        "goals.too_late": "🔒 <b>СЛИШКОМ ПОЗДНО</b>",
        "goals.too_late_text": "72 часа уже прошли.\n\nKICK остаются замороженными.",
        "goals.balance_error": "❌ <b>ОШИБКА БАЛАНСА</b>",
        "goals.balance_error_text": "Количество замороженных KICK не соответствует цели.",
        "goals.cancelled": "🗑 <b>ЦЕЛЬ ОТМЕНЕНА</b>",
        "goals.refunded": "🪙 Возвращено",
        "goals.available": "🪙 Доступно",
        "goals.in_goals": "🔒 В целях",
        "goals.continue": "Продолжаем! 💪",
        "goals.already_cancelled": "Цель уже отменена или не найдена.",

        "goals.heatmap_title": "📅 <b>ПОЛОСА ПРОГРЕССА</b>",
        "goals.heatmap_done": "выполнен",
        "goals.heatmap_missed": "пропущен",
        "goals.heatmap_pending": "предстоит",

        "goals.note_title": "📝 <b>ЧТО СДЕЛАЛ?</b>",
        "goals.note_hint": (
            "Опиши, что именно ты сделал сегодня.\n\n"
            "Например:\n"
            "<i>Пробежал 5 км за 28 минут</i>"
        ),
        "goals.note_skip": "⏭ Пропустить",
        "goals.note_saved": "✅ Записано!",

        "reminder.regular_title": "⏰ Напоминание",
        "reminder.regular_body": "Сегодняшний шаг ещё не выполнен. Успей до конца дня!",
        "reminder.warning_title": "⚠️ Внимание!",
        "reminder.warning_body": (
            "Ты пропустил один день.\n\n"
            "Если не выполнить шаг сегодня — цель закроется "
            "и станет невыполненной. KICK не вернутся."
        ),
        "goal_failed.title": "💀 ЦЕЛЬ ПРОВАЛЕНА",
        "goal_failed.body": (
            "Ты пропустил 2 дня подряд — цель закрыта как невыполненная.\n\n"
            "🔥 Не сдавайся — создай новую цель и попробуй снова."
        ),
        "goals.missed_warning_1": "⚠️ 1 пропуск — следующий пропуск закроет цель!",
        "goals.missed_warning_2": "💀 2 пропуска подряд — цель провалена",

        "ach.title": "🏆 <b>ДОСТИЖЕНИЯ</b>",
        "ach.unlocked": "✅ Получено",
        "ach.locked": "🔒 Не получено",
        "ach.new_title": "🎉 НОВОЕ ДОСТИЖЕНИЕ!",
        "ach.profile_button": "🏆 Достижения",

        # ---------- ЧЕЛЛЕНДЖИ ----------
        "ch.first_step_unavailable": "⏳ Первый шаг пока недоступен.\n\nПопробуй через",

        "ch.title": "⚔️ <b>ЧЕЛЛЕНДЖИ</b>",
        "ch.subtitle": (
            "Соревнуйся с другими игроками, "
            "выполняй цели и зарабатывай KICK!\n\n"
            "Выбери действие:"
        ),
        "ch.find_opponent": "⚔️ <b>Поиск соперника</b>",
        "ch.choose_opponent": "⚔️ <b>Выбор соперника</b>",
        "ch.no_players": "Пока нет других игроков.",
        "ch.pick_player": "Выбери игрока, которому хочешь бросить вызов:",
        "ch.opponent_not_found": "Игрок не найден.",
        "ch.insufficient_kick": (
            "⚠️ <b>Недостаточно KICK</b>\n\n"
            "Для Challenge нужно <b>{stake} KICK</b>.\n\n"
            "Твой баланс: <b>{balance} KICK</b>"
        ),
        "ch.confirm_title": "⚔️ <b>ПОДТВЕРЖДЕНИЕ CHALLENGE</b>",
        "ch.goal": "🎯 Цель",
        "ch.opponent": "👤 Соперник",
        "ch.stake": "🪙 Ставка",
        "ch.winner_gets": "🏆 Победитель получает",
        "ch.frozen_notice": "После отправки вызова ставка будет заморожена.",

        "ch.sent_title": "⚔️ <b>CHALLENGE ОТПРАВЛЕН</b>",
        "ch.await_accept": "⏳ Ожидаем принятия вызова.",

        "ch.incoming_title": "⚔️ <b>ТЕБЕ БРОСИЛИ CHALLENGE!</b>",
        "ch.player": "👤 Игрок",
        "ch.duration_label": "⏱ Длительность",
        "ch.accept_hint": "Прими вызов, чтобы начать соревнование.",
        "ch.already_exists": "Challenge уже существует.",
        "ch.not_found": "Challenge не найден.",
        "ch.not_for_you": "Этот Challenge не предназначен тебе.",
        "ch.not_yours": "Это не твой Challenge.",
        "ch.already_processed": "Challenge уже обработан.",

        "ch.accepted_title": "⚔️ <b>CHALLENGE ПРИНЯТ!</b>",
        "ch.started": "🔥 Соревнование началось!",
        "ch.creator_not_found": "Создатель Challenge не найден.",
        "ch.your_accepted": "⚔️ <b>ТВОЙ CHALLENGE ПРИНЯТ!</b>",

        "ch.declined_title": "❌ <b>CHALLENGE ОТКЛОНЁН</b>",
        "ch.you_declined": "Ты отклонил этот вызов.",
        "ch.opponent_declined_your": (
            "Соперник отклонил твой вызов.\n\n"
            "🪙 {stake} KICK возвращены."
        ),

        "ch.active_title": "⚔️ <b>АКТИВНЫЙ CHALLENGE</b>",
        "ch.pending_title": "⚔️ <b>CHALLENGE</b>",
        "ch.creator": "👤 Создатель",
        "ch.opponent_short": "⚔️ Соперник",
        "ch.pending_wait": "⏳ Ожидает принятия.",
        "ch.remaining": "⏳ Осталось",
        "ch.time_up": "⏳ <b>Время вышло</b>",
        "ch.bank": "🪙 Банк",
        "ch.you_ahead": "🔥 <b>Ты впереди!</b>",
        "ch.opponent_ahead": "⚔️ <b>Соперник впереди!</b>",
        "ch.draw_now": "🤝 <b>Сейчас ничья!</b>",
        "ch.no_access": "У тебя нет доступа к этому Challenge.",
        "ch.not_active": "Challenge уже не активен.",
        "ch.time_expired": "Время Challenge истекло.",

        "ch.finished_title": "🏁 <b>CHALLENGE ЗАВЕРШЁН</b>",
        "ch.you_win": "🏆 <b>ТЫ ПОБЕДИЛ!</b>",
        "ch.you_lose": "❌ <b>ТЫ ПРОИГРАЛ</b>",
        "ch.draw": "🤝 <b>НИЧЬЯ</b>",

        "ch.today_done": "✅ <b>Сегодняшний шаг выполнен!</b>",
        "ch.your_progress": "Твой прогресс",
        "ch.keep_going": "Продолжай завтра! 🔥",
        "ch.step_already": "Сегодняшний шаг уже выполнен.",
        "ch.all_steps_done": "Все шаги уже выполнены.",
        "ch.step_done_alert": "Шаг выполнен!",
        "ch.finished_alert": "Challenge завершён!",

        "ch.win_notification": (
            "🏆 <b>ТЫ ПОБЕДИЛ!</b>\n\n"
            "⚔️ Challenge завершён.\n\n"
            "🎯 Прогресс: <b>{progress}</b>\n\n"
            "🪙 Ты получил: <b>{reward} KICK</b>!"
        ),
        "ch.lose_notification": (
            "❌ <b>CHALLENGE ЗАВЕРШЁН</b>\n\n"
            "На этот раз победил соперник.\n\n"
            "🔥 Не останавливайся!"
        ),
        "ch.draw_notification": (
            "🤝 <b>НИЧЬЯ!</b>\n\n"
            "Оба игрока показали одинаковый результат.\n\n"
            "🪙 Тебе возвращено: <b>{stake} KICK</b>"
        ),

        "ch.history_title": "📜 <b>ИСТОРИЯ CHALLENGE</b>",
        "ch.history_empty": "История пока пуста.",
        "ch.status_win": "🏆 Победа",
        "ch.status_lose": "❌ Поражение",
        "ch.status_draw": "🤝 Ничья",
        "ch.status_declined": "❌ Отклонён",
        "ch.status_expired": "⏰ Истёк",
        "ch.status_active": "⏳ Активен",
        "ch.deleted_goal": "Удалённая цель",

        "ch.create_title": "⚔️ <b>Создание Challenge</b>",
        "ch.no_active_goals": "У тебя нет активных целей.\n\nСначала создай цель.",
        "ch.pick_goal": "Выбери цель, на основе которой хочешь создать Challenge:",
        "ch.pick_opponent_title": "⚔️ <b>ВЫБЕРИ СОПЕРНИКА</b>",
        "ch.whom": "Кому бросить вызов?",

        "ch.filter_category": "🏷 <b>Выбери категорию</b>",
        "ch.filter_all": "🔷 Все категории",
        "ch.goal_category": "🏷 Категория",
        "ch.no_opponents_category": "Нет игроков с целями в этой категории.",

        # ---------- ПРОФИЛЬ ----------
        "profile.title": "👤 <b>ПРОФИЛЬ KICK</b>",
        "profile.balance_title": "💰 <b>БАЛАНС</b>",
        "profile.available": "🪙 Доступно",
        "profile.in_goals": "🔒 В целях",
        "profile.progress_title": "📊 <b>ПРОГРЕСС</b>",
        "profile.level": "🏆 Уровень",
        "profile.xp": "⚡ XP",
        "profile.score": "⭐ SCORE",
        "profile.streak_title": "🔥 <b>STREAK</b>",
        "profile.streak_now": "🔥 Сейчас",
        "profile.streak_best": "🏅 Рекорд",
        "profile.goals_title": "🎯 <b>ЦЕЛИ</b>",
        "profile.active": "🎯 Активных",
        "profile.completed": "🏆 Завершено",
        "profile.cancelled": "❌ Отменено",
        "profile.total": "📈 Всего создано",
        "profile.user": "Пользователь",
        "profile.days_short": "дней",

        # ---------- РЕЙТИНГ ----------
        "rating.title": "🏆 <b>KICK LEADERBOARD</b>",
        "rating.top_players": "👑 <b>TOP PLAYERS</b>",
        "rating.your_result": "👤 <b>ТВОЙ РЕЗУЛЬТАТ</b>",
        "rating.place": "🏆 Место",
        "rating.level": "🏆 Уровень",
        "rating.streak_label": "🔥 Streak",
        "rating.next_opponent": "⚔️ <b>СЛЕДУЮЩИЙ СОПЕРНИК</b>",
        "rating.to_him": "🎯 До него",
        "rating.at_top": (
            "👑 <b>ТЫ НА ВЕРШИНЕ!</b>\n\n"
            "Выше тебя больше никого нет."
        ),
        "rating.path_top10": "🎯 <b>ПУТЬ В TOP 10</b>",
        "rating.to_top10": "⬆️ До TOP 10",
        "rating.keep_going": "🔥 Продолжай выполнять цели!",
        "rating.you_in_top10": "🔥 <b>ТЫ В TOP 10!</b>",
        "rating.you_in_top10_hint": "Не останавливайся — следующая позиция уже рядом. 🚀",
        "rating.metric_streak": "🔥 STREAK",
        "rating.metric_score": "⭐ SCORE",
        "rating.metric_xp": "⚡ XP",
        "rating.days_short": "дн.",

        # ---------- НАСТРОЙКИ ----------
        "settings.title": "⚙️ <b>НАСТРОЙКИ</b>",
        "settings.choose": "Что хочешь настроить?",
        "settings.notifications": "🔔 Уведомления",
        "settings.language": "🌐 Язык",
        "settings.data": "🗑 Данные",
        "settings.back": "🔙 Назад",
        "settings.main_menu": "🏠 Главное меню",
        "settings.notifications_title": "🔔 <b>УВЕДОМЛЕНИЯ</b>",
        "settings.goal_notifications": "🎯 Цели",
        "settings.challenge_notifications": "⚔️ Челленджи",
        "settings.achievement_notifications": "🏆 Достижения",
        "settings.choose_language": "🌐 <b>ВЫБОР ЯЗЫКА</b>",
        "settings.language_changed": "✅ Язык изменён.",
        "settings.data_title": "🗑 <b>УПРАВЛЕНИЕ ДАННЫМИ</b>",
        "settings.data_description": "Выбери действие:",
        "settings.delete_goals": "🗑 Удалить все цели",
        "settings.reset_progress": "🔄 Сбросить прогресс",
        "settings.delete_account": "❌ Удалить аккаунт",
        "settings.confirm_delete": "✅ Удалить",
        "settings.cancel": "❌ Отмена",
        "settings.delete_goals_warning": (
            "⚠️ <b>УДАЛИТЬ ВСЕ ЦЕЛИ?</b>\n\n"
            "Все цели и связанные челленджи будут удалены.\n"
            "Действие необратимо."
        ),
        "settings.confirm_delete_goals": "✅ Да, удалить",
        "settings.reset_progress_warning": (
            "⚠️ <b>СБРОСИТЬ ПРОГРЕСС?</b>\n\n"
            "XP, уровень, score и streak будут сброшены."
        ),
        "settings.confirm_reset_progress": "✅ Да, сбросить",
        "settings.goals_deleted": "✅ Все цели удалены.",
        "settings.progress_reset": "✅ Прогресс сброшен.",
        "settings.main_menu_text": "🏠 Главное меню",
    },

    # ========================================================
    # ENGLISH
    # ========================================================
    "en": {
        # ---------------- HELP ----------------
        "menu.help": "❓ Help",

                # ---------- MENU: BONUS ----------
        "menu.bonus": "🎁 Bonus",

        # ---------- BONUS ----------
        "bonus.title": "🎁 <b>BONUSES</b>",
        "bonus.subtitle": (
            "Complete tasks and get free KICK!\n\n"
            "Choose a task 👇"
        ),

        "bonus.channel_title": "📢 <b>CHANNEL SUBSCRIPTION</b>",
        "bonus.channel_body": (
            "Subscribe to our channel and get "
            "<b>+50 KICK</b> on your balance.\n\n"
            "After subscribing, tap '✅ Check'.\n\n"
            "🔗 <a href=\"https://t.me/kickgame_official\">kickgame_official</a>"
        ),
        "bonus.channel_button": "✅ Check",
        "bonus.channel_button_go": "📢 Subscribe",
        "bonus.channel_claimed": (
            "✅ You've already received the subscription reward.\n\n"
            "Come back for other bonuses!"
        ),
        "bonus.channel_success": (
            "🎉 <b>+50 KICK</b>\n\n"
            "Thanks for subscribing! Reward credited."
        ),
        "bonus.channel_not_subscribed": (
            "⚠️ You haven't subscribed to the channel yet.\n\n"
            "Subscribe and tap 'Check' again."
        ),
        "bonus.channel_check_error": (
            "❌ Could not check subscription. Try again later."
        ),

        "bonus.streak3_title": "🔥 <b>3 DAYS IN A ROW</b>",
        "bonus.streak3_body": (
            "Complete any task 3 days in a row and get "
            "<b>+10 KICK</b>.\n\n"
            "Can be claimed once a week."
        ),
        "bonus.streak5_title": "⚡ <b>5 DAYS IN A ROW</b>",
        "bonus.streak5_body": (
            "Complete any task 5 days in a row and get "
            "<b>+30 KICK</b>.\n\n"
            "Can be claimed once a week."
        ),

        "bonus.claim_button": "🎁 Claim",
        "bonus.claimed_today": "✅ Already claimed. Come back later.",
        "bonus.not_enough_streak": (
            "⚠️ You haven't completed the requirement yet.\n\n"
            "Your streak: <b>{streak}</b>"
        ),
        "bonus.claim_success": (
            "🎉 <b>+{amount} KICK</b>\n\n"
            "Reward credited!"
        ),
        "bonus.week_wait": (
            "⏳ Next reward will be available later."
        ),

        "bonus.back": "🔙 To bonuses",
        
        "help.title": "❓ <b>HOW TO PLAY KICK</b>",
        "help.body": (
            "⚡ <b>KICK</b> is a game where your goals become a competition.\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🎯 <b>GOALS</b>\n"
            "• Create a goal and pick a duration\n"
            "• Mark your step every day\n"
            "• 2 missed days in a row — goal fails, KICK burns\n\n"
            "🪙 <b>KICK</b>\n"
            "• Starting balance — 100 KICK\n"
            "• Part of your KICK is frozen on goal creation\n"
            "• Complete the goal — KICK returned + reward\n"
            "• Fail — KICK are not returned\n\n"
            "⚔️ <b>CHALLENGES</b>\n"
            "• Challenge another player\n"
            "• Both stake KICK, the winner takes the bank\n\n"
            "🔥 <b>STREAK</b>\n"
            "• Mark steps every day\n"
            "• The longer your streak — the bigger your rewards\n\n"
            "🏆 <b>ACHIEVEMENTS</b>\n"
            "• Unlocked for progress, streaks and wins\n"
            "• See them in your profile\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🔥 Don't give up — KICK is waiting!"
        ),
        "help.commands": (
            "⚙️ <b>Commands</b>\n\n"
            "/start — main menu\n"
            "/help — this help\n"
            "/cancel — cancel current action"
        ),
        "help.cancelled": "✅ Action cancelled.",

        # ---------------- BUTTONS ----------------
        "btn.duration.1": "1 day",
        "btn.duration.3": "3 days",
        "btn.duration.7": "7 days",
        "btn.duration.14": "14 days",
        "btn.duration.30": "30 days",
        "btn.duration.90": "90 days",
        "btn.duration.custom": "✏️ Custom",

        "btn.start": "🚀 Start",
        "btn.edit": "✏️ Edit",
        "btn.cancel": "❌ Cancel",

        "btn.edit_title": "🎯 Title",
        "btn.edit_category": "🏷 Category",
        "btn.edit_description": "📝 Why I want this",
        "btn.edit_result": "🎯 What I want to achieve",
        "btn.edit_duration": "⏱ Duration",

        "btn.skip": "⏭ Skip",
        "btn.back": "🔙 Back",
        "btn.back_to_goal": "🔙 To goal",
        "btn.back_to_goals": "🔙 To goals list",
        "btn.back_to_challenges": "🔙 To challenges",
        "btn.back_to_challenge": "🔙 To challenge",

        "btn.create_goal": "➕ Create goal",
        "btn.find_opponent": "⚔️ Find opponent",
        "btn.complete_today": "✅ Complete today's step",
        "btn.complete_today_short": "✅ Complete today",
        "btn.heatmap": "📅 Progress bar",
        "btn.all_steps": "📋 All steps",
        "btn.cancel_goal": "🗑 Cancel goal",
        "btn.yes_cancel": "🗑 Yes, cancel",
        "btn.no_back": "🔙 No, go back",

        "btn.throw_challenge": "⚔️ Send challenge",
        "btn.choose_other": "🔙 Choose another",
        "btn.accept": "⚔️ Accept challenge",
        "btn.decline": "❌ Decline",
        "btn.open_challenge": "⚔️ Open challenge",
        "btn.refresh": "🔄 Refresh",
        "btn.create_challenge": "⚔️ Create challenge",
        "btn.history": "📜 Challenge history",
        "btn.filter_all": "🔷 All categories",

        # ---------------- CATEGORIES ----------------
        "category.title": "🏷 <b>CHOOSE CATEGORY</b>",
        "category.hint": "Which area does your goal belong to?",

        # ---------- MAIN MENU ----------
        "menu.my_goals": "🎯 My goals",
        "menu.profile": "👤 Profile",
        "menu.rating": "🏆 Rating",
        "menu.challenges": "⚔️ Challenges",
        "menu.ai_coach": "🤖 AI Coach",
        "menu.settings": "⚙️ Settings",

        "common.back": "🔙 Back",
        "common.cancel": "❌ Cancel",
        "common.yes": "✅ Yes",
        "common.no": "❌ No",
        "common.user_not_found": "User not found.",
        "common.goal_not_found": "Goal not found.",
        "common.player": "Player",
        "common.days": "days",
        "common.hours_short": "h.",
        "common.minutes_short": "min.",

        "goals.title": "🎯 <b>MY GOALS</b>",
        "goals.no_goals": (
            "You don't have any active goals yet.\n\n"
            "Create your first goal and start moving forward! 🚀"
        ),
        "goals.choose": "Choose a goal:",

        "goals.new": "🎯 <b>NEW GOAL</b>",
        "goals.choose_duration": (
            "First, choose the goal duration.\n\n"
            "The longer the goal, the higher the potential reward.\n\n"
            "💡 Part of your KICK will be frozen after creation."
        ),
        "goals.custom_duration": "⏱ <b>CUSTOM DURATION</b>",
        "goals.enter_days": "Enter the number of days.\n\nFor example:\n<code>45</code>",
        "goals.enter_days_number": "Enter the number of days.",
        "goals.min_duration": "Duration must be at least 1 day.",
        "goals.max_duration": "Maximum duration is 365 days.",
        "goals.enter_title": (
            "🎯 <b>GOAL TITLE</b>\n\n"
            "Write what you want to achieve.\n\n"
            "For example:\n"
            "<i>Learn Python</i>\n"
            "<i>Exercise every day</i>\n"
            "<i>Read 5 books</i>"
        ),
        "goals.title_empty": "Goal title cannot be empty.",
        "goals.title_too_long": "Goal title is too long.",

        "goals.duration_label": "⏱ Duration",
        "goals.difficulty_label": "🔥 Difficulty",
        "goals.difficulty_hard": "hard",
        "goals.difficulty_normal": "normal",
        "goals.preview": "🚀 <b>GOAL PREVIEW</b>",
        "goals.conditions": "💰 <b>CONDITIONS</b>",
        "goals.freeze": "🔒 Freeze",
        "goals.reward": "🪙 Reward",
        "goals.balance": "🪙 Your balance",
        "goals.cancel_72": (
            "After starting a goal, you can cancel it only "
            "within the first 72 hours."
        ),

        "goals.enter_description": (
            "📝 <b>GOAL DESCRIPTION</b>\n\n"
            "Briefly describe why you want this.\n\n"
            "For example:\n"
            "<i>I want to become a backend developer by summer</i>\n\n"
            "Or tap 'Skip'."
        ),
        "goals.description_label": "📝 Description",
        "goals.new_description": "✏️ <b>NEW DESCRIPTION</b>",
        "goals.enter_new_description": "Write a new description.",
        "goals.edit_description": "📝 Description",

        "goals.enter_result": (
            "🎯 <b>WHAT RESULT DO YOU WANT?</b>\n\n"
            "Describe briefly and concretely what "
            "should be achieved at the end.\n\n"
            "For example:\n"
            "<i>Run 10 km without stopping</i>\n"
            "<i>Pass IELTS with 7.0</i>\n"
            "<i>Write 30,000 words of a novel</i>\n\n"
            "Or tap 'Skip'."
        ),
        "goals.result_label": "🎯 Result",
        "goals.new_result": "✏️ <b>NEW RESULT</b>",
        "goals.enter_new_result": "Describe the new result.",
        "goals.edit_result": "🎯 Result",

        "goals.editing": "✏️ <b>EDITING</b>",
        "goals.what_edit": "What do you want to change?",
        "goals.new_title": "✏️ <b>NEW TITLE</b>",
        "goals.enter_new_title": "Enter a new goal title.",
        "goals.new_duration": "⏱ <b>NEW DURATION</b>",
        "goals.choose_new_duration": "Choose a new duration:",

        "goals.started": "🚀 <b>GOAL STARTED!</b>",
        "goals.first_step_wait": "🔥 Your first step is waiting!",
        "goals.remember_cancel": (
            "Remember: you can cancel the goal only "
            "within the first 72 hours."
        ),

        "goals.insufficient_kick": "❌ <b>NOT ENOUGH KICK</b>",
        "goals.need_kick": "This goal requires",
        "goals.data_lost": "Goal data was lost.",
        "goals.creation_cancelled": "❌ <b>GOAL CREATION CANCELLED.</b>",
        "goals.can_create_again": "You can create a new goal anytime.",
        "goals.active_not_found": "Active goal not found.",

        "goals.status_active": "🟢 Active",
        "goals.status_completed": "🏆 Completed",
        "goals.status_cancelled": "❌ Cancelled",
        "goals.status_failed": "💀 Failed",

        "goals.progress": "📈 Progress",
        "goals.completed": "✅ Completed",
        "goals.frozen": "🔒 Frozen",
        "goals.cancel_available": "🗑 Cancellation available for",
        "goals.cancel_unavailable": "🔒 <b>Cancellation unavailable</b>",

        "goals.step_not_found": "Today's step was not found.",
        "goals.step_already_done": "Today's step is already completed! ✅",
        "goals.first_step_unavailable": (
            "⏳ The first step is not available yet.\n\n"
            "Try again in"
        ),

        "goals.completed_title": "🏆 <b>GOAL COMPLETED!</b>",
        "goals.all_steps_done": "🔥 All steps completed!",
        "goals.step_reward": "🪙 Reward",
        "goals.xp": "⚡ XP",
        "goals.step_completed": "✅ <b>STEP COMPLETED!</b>",
        "goals.day": "📅 Day",
        "goals.level_up": "🎉 <b>LEVEL UP!</b>",
        "goals.new_level": "🏆 New level",

        "goals.steps": "📋 <b>GOAL STEPS</b>",
        "goals.day_word": "Day",

        "goals.cancel_confirm": "🗑 <b>CANCEL GOAL?</b>",
        "goals.returned": "🔒 Returned",
        "goals.cancel_info": (
            "The goal will be cancelled and will no longer be active."
        ),
        "goals.cancel_unavailable_title": "🔒 <b>CANCELLATION UNAVAILABLE</b>",
        "goals.cancel_72_passed": (
            "72 hours since the goal was created have passed.\n\n"
            "You can only continue the goal now."
        ),
        "goals.too_late": "🔒 <b>TOO LATE</b>",
        "goals.too_late_text": (
            "72 hours have already passed.\n\n"
            "Your KICK remains frozen."
        ),
        "goals.balance_error": "❌ <b>BALANCE ERROR</b>",
        "goals.balance_error_text": (
            "The amount of frozen KICK does not match this goal."
        ),
        "goals.cancelled": "🗑 <b>GOAL CANCELLED</b>",
        "goals.refunded": "🪙 Refunded",
        "goals.available": "🪙 Available",
        "goals.in_goals": "🔒 In goals",
        "goals.continue": "Keep going! 💪",
        "goals.already_cancelled": "The goal was already cancelled or not found.",

        "goals.heatmap_title": "📅 <b>PROGRESS BAR</b>",
        "goals.heatmap_done": "completed",
        "goals.heatmap_missed": "missed",
        "goals.heatmap_pending": "upcoming",

        "goals.note_title": "📝 <b>WHAT DID YOU DO?</b>",
        "goals.note_hint": (
            "Describe what exactly you did today.\n\n"
            "For example:\n"
            "<i>Ran 5 km in 28 minutes</i>"
        ),
        "goals.note_skip": "⏭ Skip",
        "goals.note_saved": "✅ Saved!",

        "reminder.regular_title": "⏰ Reminder",
        "reminder.regular_body": "Today's step is not completed yet. Do it before the day ends!",
        "reminder.warning_title": "⚠️ Warning!",
        "reminder.warning_body": (
            "You missed one day.\n\n"
            "If you don't complete today's step — the goal will be closed "
            "as failed. KICK won't be refunded."
        ),
        "goal_failed.title": "💀 GOAL FAILED",
        "goal_failed.body": (
            "You missed 2 days in a row — the goal was closed as failed.\n\n"
            "🔥 Don't give up — create a new goal and try again."
        ),
        "goals.missed_warning_1": "⚠️ 1 miss — next miss will close the goal!",
        "goals.missed_warning_2": "💀 2 misses in a row — goal failed",

        "ach.title": "🏆 <b>ACHIEVEMENTS</b>",
        "ach.unlocked": "✅ Unlocked",
        "ach.locked": "🔒 Locked",
        "ach.new_title": "🎉 NEW ACHIEVEMENT!",
        "ach.profile_button": "🏆 Achievements",

        # ---------- CHALLENGES ----------
        "ch.first_step_unavailable": "⏳ The first step is not available yet.\n\nTry again in",

        "ch.title": "⚔️ <b>CHALLENGES</b>",
        "ch.subtitle": (
            "Compete with other players, "
            "complete goals and earn KICK!\n\n"
            "Choose an action:"
        ),
        "ch.find_opponent": "⚔️ <b>Find opponent</b>",
        "ch.choose_opponent": "⚔️ <b>Choose opponent</b>",
        "ch.no_players": "No other players yet.",
        "ch.pick_player": "Choose the player you want to challenge:",
        "ch.opponent_not_found": "Player not found.",
        "ch.insufficient_kick": (
            "⚠️ <b>Not enough KICK</b>\n\n"
            "Challenge requires <b>{stake} KICK</b>.\n\n"
            "Your balance: <b>{balance} KICK</b>"
        ),
        "ch.confirm_title": "⚔️ <b>CHALLENGE CONFIRMATION</b>",
        "ch.goal": "🎯 Goal",
        "ch.opponent": "👤 Opponent",
        "ch.stake": "🪙 Stake",
        "ch.winner_gets": "🏆 Winner gets",
        "ch.frozen_notice": "After sending the challenge, the stake will be frozen.",

        "ch.sent_title": "⚔️ <b>CHALLENGE SENT</b>",
        "ch.await_accept": "⏳ Waiting for acceptance.",

        "ch.incoming_title": "⚔️ <b>YOU GOT A CHALLENGE!</b>",
        "ch.player": "👤 Player",
        "ch.duration_label": "⏱ Duration",
        "ch.accept_hint": "Accept to start the competition.",
        "ch.already_exists": "Challenge already exists.",
        "ch.not_found": "Challenge not found.",
        "ch.not_for_you": "This challenge is not for you.",
        "ch.not_yours": "This is not your challenge.",
        "ch.already_processed": "Challenge already processed.",

        "ch.accepted_title": "⚔️ <b>CHALLENGE ACCEPTED!</b>",
        "ch.started": "🔥 Competition started!",
        "ch.creator_not_found": "Challenge creator not found.",
        "ch.your_accepted": "⚔️ <b>YOUR CHALLENGE WAS ACCEPTED!</b>",

        "ch.declined_title": "❌ <b>CHALLENGE DECLINED</b>",
        "ch.you_declined": "You declined this challenge.",
        "ch.opponent_declined_your": (
            "Your opponent declined your challenge.\n\n"
            "🪙 {stake} KICK refunded."
        ),

        "ch.active_title": "⚔️ <b>ACTIVE CHALLENGE</b>",
        "ch.pending_title": "⚔️ <b>CHALLENGE</b>",
        "ch.creator": "👤 Creator",
        "ch.opponent_short": "⚔️ Opponent",
        "ch.pending_wait": "⏳ Waiting for acceptance.",
        "ch.remaining": "⏳ Remaining",
        "ch.time_up": "⏳ <b>Time's up</b>",
        "ch.bank": "🪙 Bank",
        "ch.you_ahead": "🔥 <b>You're ahead!</b>",
        "ch.opponent_ahead": "⚔️ <b>Opponent is ahead!</b>",
        "ch.draw_now": "🤝 <b>It's a draw!</b>",
        "ch.no_access": "You don't have access to this challenge.",
        "ch.not_active": "Challenge is no longer active.",
        "ch.time_expired": "Challenge time expired.",

        "ch.finished_title": "🏁 <b>CHALLENGE FINISHED</b>",
        "ch.you_win": "🏆 <b>YOU WON!</b>",
        "ch.you_lose": "❌ <b>YOU LOST</b>",
        "ch.draw": "🤝 <b>DRAW</b>",

        "ch.today_done": "✅ <b>Today's step completed!</b>",
        "ch.your_progress": "Your progress",
        "ch.keep_going": "Keep going tomorrow! 🔥",
        "ch.step_already": "Today's step is already completed.",
        "ch.all_steps_done": "All steps already completed.",
        "ch.step_done_alert": "Step completed!",
        "ch.finished_alert": "Challenge finished!",

        "ch.win_notification": (
            "🏆 <b>YOU WON!</b>\n\n"
            "⚔️ Challenge finished.\n\n"
            "🎯 Progress: <b>{progress}</b>\n\n"
            "🪙 You received: <b>{reward} KICK</b>!"
        ),
        "ch.lose_notification": (
            "❌ <b>CHALLENGE FINISHED</b>\n\n"
            "Your opponent won this time.\n\n"
            "🔥 Don't stop!"
        ),
        "ch.draw_notification": (
            "🤝 <b>DRAW!</b>\n\n"
            "Both players showed the same result.\n\n"
            "🪙 Refunded: <b>{stake} KICK</b>"
        ),

        "ch.history_title": "📜 <b>CHALLENGE HISTORY</b>",
        "ch.history_empty": "History is empty.",
        "ch.status_win": "🏆 Win",
        "ch.status_lose": "❌ Loss",
        "ch.status_draw": "🤝 Draw",
        "ch.status_declined": "❌ Declined",
        "ch.status_expired": "⏰ Expired",
        "ch.status_active": "⏳ Active",
        "ch.deleted_goal": "Deleted goal",

        "ch.create_title": "⚔️ <b>Create Challenge</b>",
        "ch.no_active_goals": "You don't have active goals.\n\nCreate a goal first.",
        "ch.pick_goal": "Choose a goal to base the challenge on:",
        "ch.pick_opponent_title": "⚔️ <b>CHOOSE OPPONENT</b>",
        "ch.whom": "Who to challenge?",

        "ch.filter_category": "🏷 <b>Choose category</b>",
        "ch.filter_all": "🔷 All categories",
        "ch.goal_category": "🏷 Category",
        "ch.no_opponents_category": "No players with goals in this category.",

        "profile.title": "👤 <b>KICK PROFILE</b>",
        "profile.balance_title": "💰 <b>BALANCE</b>",
        "profile.available": "🪙 Available",
        "profile.in_goals": "🔒 In goals",
        "profile.progress_title": "📊 <b>PROGRESS</b>",
        "profile.level": "🏆 Level",
        "profile.xp": "⚡ XP",
        "profile.score": "⭐ SCORE",
        "profile.streak_title": "🔥 <b>STREAK</b>",
        "profile.streak_now": "🔥 Current",
        "profile.streak_best": "🏅 Best",
        "profile.goals_title": "🎯 <b>GOALS</b>",
        "profile.active": "🎯 Active",
        "profile.completed": "🏆 Completed",
        "profile.cancelled": "❌ Cancelled",
        "profile.total": "📈 Total created",
        "profile.user": "User",
        "profile.days_short": "days",

        "rating.title": "🏆 <b>KICK LEADERBOARD</b>",
        "rating.top_players": "👑 <b>TOP PLAYERS</b>",
        "rating.your_result": "👤 <b>YOUR RESULT</b>",
        "rating.place": "🏆 Place",
        "rating.level": "🏆 Level",
        "rating.streak_label": "🔥 Streak",
        "rating.next_opponent": "⚔️ <b>NEXT OPPONENT</b>",
        "rating.to_him": "🎯 To him",
        "rating.at_top": (
            "👑 <b>YOU'RE AT THE TOP!</b>\n\n"
            "Nobody is above you."
        ),
        "rating.path_top10": "🎯 <b>PATH TO TOP 10</b>",
        "rating.to_top10": "⬆️ To TOP 10",
        "rating.keep_going": "🔥 Keep completing goals!",
        "rating.you_in_top10": "🔥 <b>YOU'RE IN TOP 10!</b>",
        "rating.you_in_top10_hint": "Don't stop — the next position is close. 🚀",
        "rating.metric_streak": "🔥 STREAK",
        "rating.metric_score": "⭐ SCORE",
        "rating.metric_xp": "⚡ XP",
        "rating.days_short": "d.",

        "settings.title": "⚙️ <b>SETTINGS</b>",
        "settings.choose": "What do you want to configure?",
        "settings.notifications": "🔔 Notifications",
        "settings.language": "🌐 Language",
        "settings.data": "🗑 Data",
        "settings.back": "🔙 Back",
        "settings.main_menu": "🏠 Main menu",
        "settings.notifications_title": "🔔 <b>NOTIFICATIONS</b>",
        "settings.goal_notifications": "🎯 Goals",
        "settings.challenge_notifications": "⚔️ Challenges",
        "settings.achievement_notifications": "🏆 Achievements",
        "settings.choose_language": "🌐 <b>CHOOSE LANGUAGE</b>",
        "settings.language_changed": "✅ Language changed.",
        "settings.data_title": "🗑 <b>DATA MANAGEMENT</b>",
        "settings.data_description": "Choose an action:",
        "settings.delete_goals": "🗑 Delete all goals",
        "settings.reset_progress": "🔄 Reset progress",
        "settings.delete_account": "❌ Delete account",
        "settings.confirm_delete": "✅ Delete",
        "settings.cancel": "❌ Cancel",
        "settings.delete_goals_warning": (
            "⚠️ <b>DELETE ALL GOALS?</b>\n\n"
            "All goals and related challenges will be deleted.\n"
            "This action is irreversible."
        ),
        "settings.confirm_delete_goals": "✅ Yes, delete",
        "settings.reset_progress_warning": (
            "⚠️ <b>RESET PROGRESS?</b>\n\n"
            "XP, level, score and streak will be reset."
        ),
        "settings.confirm_reset_progress": "✅ Yes, reset",
        "settings.goals_deleted": "✅ All goals deleted.",
        "settings.progress_reset": "✅ Progress reset.",
        "settings.main_menu_text": "🏠 Main menu",
    },

    # ========================================================
    # ARMENIAN
    # ========================================================
    "hy": {
        # ---------------- HELP ----------------
        "menu.help": "❓ Օգնություն",
                # ---------- MENU: BONUS ----------
        "menu.bonus": "🎁 Բոնուս",

        # ---------- BONUS ----------
        "bonus.title": "🎁 <b>ԲՈՆՈՒՍՆԵՐ</b>",
        "bonus.subtitle": (
            "Կատարեք առաջադրանքները և ստացեք KICK անվճար!\n\n"
            "Ընտրեք առաջադրանք 👇"
        ),

        "bonus.channel_title": "📢 <b>ԲԱԺԱՆՈՐԴԱԳՐՈՒԹՅՈՒՆ</b>",
        "bonus.channel_body": (
            "Բաժանորդագրվեք մեր ալիքին և ստացեք "
            "<b>+50 KICK</b>։\n\n"
            "Բաժանորդագրվելուց հետո սեղմեք «✅ Ստուգել»։\n\n"
            "🔗 <a href=\"https://t.me/kickgame_official\">kickgame_official</a>"
        ),
        "bonus.channel_button": "✅ Ստուգել",
        "bonus.channel_button_go": "📢 Բաժանորդագրվել",
        "bonus.channel_claimed": (
            "✅ Դուք արդեն ստացել եք բաժանորդագրության պարգևը։\n\n"
            "Վերադարձեք այլ բոնուսների համար։"
        ),
        "bonus.channel_success": (
            "🎉 <b>+50 KICK</b>\n\n"
            "Շնորհակալություն բաժանորդագրվելու համար։"
        ),
        "bonus.channel_not_subscribed": (
            "⚠️ Դեռ բաժանորդագրված չեք։\n\n"
            "Բաժանորդագրվեք և նորից սեղմեք «Ստուգել»։"
        ),
        "bonus.channel_check_error": (
            "❌ Չհաջողվեց ստուգել բաժանորդագրությունը։"
        ),

        "bonus.streak3_title": "🔥 <b>3 ՕՐ ԱՆԸՆԴՄԵՋ</b>",
        "bonus.streak3_body": (
            "Կատարեք ցանկացած առաջադրանք 3 օր անընդմեջ և ստացեք "
            "<b>+10 KICK</b>։\n\n"
            "Կարելի է ստանալ շաբաթը մեկ անգամ։"
        ),
        "bonus.streak5_title": "⚡ <b>5 ՕՐ ԱՆԸՆԴՄԵՋ</b>",
        "bonus.streak5_body": (
            "Կատարեք ցանկացած առաջադրանք 5 օր անընդմեջ և ստացեք "
            "<b>+30 KICK</b>։\n\n"
            "Կարելի է ստանալ շաբաթը մեկ անգամ։"
        ),

        "bonus.claim_button": "🎁 Ստանալ",
        "bonus.claimed_today": "✅ Արդեն ստացված է։ Վերադարձեք ավելի ուշ։",
        "bonus.not_enough_streak": (
            "⚠️ Դեռ չեք կատարել պայմանը։\n\n"
            "Ձեր streak-ը՝ <b>{streak}</b>"
        ),
        "bonus.claim_success": (
            "🎉 <b>+{amount} KICK</b>\n\n"
            "Պարգևը մուտքագրված է։"
        ),
        "bonus.week_wait": (
            "⏳ Հաջորդ պարգևը կհասանելի լինի ավելի ուշ։"
        ),

        "bonus.back": "🔙 Դեպի բոնուսներ",
        "help.title": "❓ <b>ԻՆՉՊԵՍ ԽԱՂԱԼ KICK</b>",
        "help.body": (
            "⚡ <b>KICK</b> — խաղ, որտեղ ձեր նպատակները դառնում են մրցույթ։\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🎯 <b>ՆՊԱՏԱԿՆԵՐ</b>\n"
            "• Ստեղծեք նպատակ և ընտրեք տևողություն\n"
            "• Ամեն օր նշեք քայլը\n"
            "• 2 բացթողում անընդմեջ — նպատակը ձախողվում է, KICK-ը այրվում\n\n"
            "🪙 <b>KICK</b>\n"
            "• Սկզբնական հաշվեկշիռը — 100 KICK\n"
            "• Նպատակ ստեղծելիս KICK-ի մի մասը սառեցվում է\n"
            "• Ավարտեցիք նպատակը — KICK-ը վերադարձվում է + պարգև\n"
            "• Ձախողվեց — KICK-ը չի վերադարձվում\n\n"
            "⚔️ <b>ՉԵԼԵՆՋՆԵՐ</b>\n"
            "• Մարտահրավեր նետեք այլ խաղացողի\n"
            "• Երկուսն էլ դնում են խաղադրույք, հաղթողը վերցնում է բանկը\n\n"
            "🔥 <b>STREAK</b>\n"
            "• Ամեն օր նշեք քայլերը\n"
            "• Որքան երկար է streak-ը, այնքան մեծ է պարգևը\n\n"
            "🏆 <b>ՁԵՌՔԲԵՐՈՒՄՆԵՐ</b>\n"
            "• Բացվում են առաջընթացի, streak-ի և հաղթանակների համար\n"
            "• Դիտեք դրանք պրոֆիլում\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🔥 Մի՛ հանձնվեք — KICK-ը սպասում է!"
        ),
        "help.commands": (
            "⚙️ <b>Հրամաններ</b>\n\n"
            "/start — գլխավոր մենյու\n"
            "/help — այս օգնությունը\n"
            "/cancel — չեղարկել գործողությունը"
        ),
        "help.cancelled": "✅ Գործողությունը չեղարկվեց։",

        # ---------------- ԿՈՃԱԿՆԵՐ ----------------
        "btn.duration.1": "1 օր",
        "btn.duration.3": "3 օր",
        "btn.duration.7": "7 օր",
        "btn.duration.14": "14 օր",
        "btn.duration.30": "30 օր",
        "btn.duration.90": "90 օր",
        "btn.duration.custom": "✏️ Սեփական",

        "btn.start": "🚀 Սկսել",
        "btn.edit": "✏️ Խմբագրել",
        "btn.cancel": "❌ Չեղարկել",

        "btn.edit_title": "🎯 Անվանում",
        "btn.edit_category": "🏷 Կարգ",
        "btn.edit_description": "📝 Ինչու եմ ուզում",
        "btn.edit_result": "🎯 Ինչի ուզում եմ հասնել",
        "btn.edit_duration": "⏱ Տևողություն",

        "btn.skip": "⏭ Բաց թողնել",
        "btn.back": "🔙 Հետ",
        "btn.back_to_goal": "🔙 Դեպի նպատակ",
        "btn.back_to_goals": "🔙 Դեպի նպատակների ցանկ",
        "btn.back_to_challenges": "🔙 Դեպի չելենջներ",
        "btn.back_to_challenge": "🔙 Դեպի չելենջ",

        "btn.create_goal": "➕ Ստեղծել նպատակ",
        "btn.find_opponent": "⚔️ Գտնել մրցակից",
        "btn.complete_today": "✅ Կատարել այսօրվա քայլը",
        "btn.complete_today_short": "✅ Կատարել այսօր",
        "btn.heatmap": "📅 Առաջընթացի գոտի",
        "btn.all_steps": "📋 Բոլոր քայլերը",
        "btn.cancel_goal": "🗑 Չեղարկել նպատակը",
        "btn.yes_cancel": "🗑 Այո, չեղարկել",
        "btn.no_back": "🔙 Ոչ, վերադառնալ",

        "btn.throw_challenge": "⚔️ Ուղարկել մարտահրավեր",
        "btn.choose_other": "🔙 Ընտրել ուրիշին",
        "btn.accept": "⚔️ Ընդունել",
        "btn.decline": "❌ Մերժել",
        "btn.open_challenge": "⚔️ Բացել չելենջ",
        "btn.refresh": "🔄 Թարմացնել",
        "btn.create_challenge": "⚔️ Ստեղծել չելենջ",
        "btn.history": "📜 Չելենջների պատմություն",
        "btn.filter_all": "🔷 Բոլոր կարգերը",

        # ---------------- ԿԱՐԳԵՐ ----------------
        "category.title": "🏷 <b>ԸՆՏՐԵՔ ԿԱՐԳԸ</b>",
        "category.hint": "Ո՞ր ոլորտին է պատկանում ձեր նպատակը։",

        "menu.my_goals": "🎯 Իմ նպատակները",
        "menu.profile": "👤 Պրոֆիլ",
        "menu.rating": "🏆 Վարկանիշ",
        "menu.challenges": "⚔️ Չելենջներ",
        "menu.ai_coach": "🤖 AI Coach",
        "menu.settings": "⚙️ Կարգավորումներ",

        "common.back": "🔙 Հետ",
        "common.cancel": "❌ Չեղարկել",
        "common.yes": "✅ Այո",
        "common.no": "❌ Ոչ",
        "common.user_not_found": "Օգտատերը չի գտնվել։",
        "common.goal_not_found": "Նպատակը չի գտնվել։",
        "common.player": "Խաղացող",
        "common.days": "օր",
        "common.hours_short": "ժ.",
        "common.minutes_short": "ր.",

        "goals.title": "🎯 <b>ԻՄ ՆՊԱՏԱԿՆԵՐԸ</b>",
        "goals.no_goals": (
            "Դեռ չունեք ակտիվ նպատակներ։\n\n"
            "Ստեղծեք ձեր առաջին նպատակը և սկսեք առաջ շարժվել։ 🚀"
        ),
        "goals.choose": "Ընտրեք նպատակ։",

        "goals.new": "🎯 <b>ՆՈՐ ՆՊԱՏԱԿ</b>",
        "goals.choose_duration": (
            "Սկզբում ընտրեք նպատակի տևողությունը։\n\n"
            "Որքան երկար է նպատակը, այնքան բարձր է հնարավոր պարգևը։\n\n"
            "💡 Ստեղծելուց հետո KICK-ի մի մասը կսառեցվի։"
        ),
        "goals.custom_duration": "⏱ <b>ՍԵՓԱԿԱՆ ՏԵՎՈՂՈՒԹՅՈՒՆ</b>",
        "goals.enter_days": "Մուտքագրեք օրերի քանակը։\n\nՕրինակ՝\n<code>45</code>",
        "goals.enter_days_number": "Մուտքագրեք օրերի քանակը։",
        "goals.min_duration": "Տևողությունը պետք է լինի առնվազն 1 օր։",
        "goals.max_duration": "Առավելագույն տևողությունը 365 օր է։",
        "goals.enter_title": (
            "🎯 <b>ՆՊԱՏԱԿԻ ԱՆՎԱՆՈՒՄ</b>\n\n"
            "Գրեք, թե ինչի եք ցանկանում հասնել։\n\n"
            "Օրինակ՝\n"
            "<i>Սովորել Python</i>\n"
            "<i>Մարզվել ամեն օր</i>\n"
            "<i>Կարդալ 5 գիրք</i>"
        ),
        "goals.title_empty": "Անվանումը չի կարող դատարկ լինել։",
        "goals.title_too_long": "Նպատակի անվանումը չափազանց երկար է։",

        "goals.duration_label": "⏱ Տևողություն",
        "goals.difficulty_label": "🔥 Բարդություն",
        "goals.difficulty_hard": "բարդ",
        "goals.difficulty_normal": "սովորական",
        "goals.preview": "🚀 <b>ՆՊԱՏԱԿԻ ՆԱԽԱԴԻՏՈՒՄ</b>",
        "goals.conditions": "💰 <b>ՊԱՅՄԱՆՆԵՐ</b>",
        "goals.freeze": "🔒 Սառեցում",
        "goals.reward": "🪙 Պարգև",
        "goals.balance": "🪙 Ձեր հաշվեկշիռը",
        "goals.cancel_72": (
            "Նպատակը սկսելուց հետո այն կարող եք չեղարկել "
            "միայն առաջին 72 ժամվա ընթացքում։"
        ),

        "goals.enter_description": (
            "📝 <b>ՆՊԱՏԱԿԻ ՆԿԱՐԱԳՐՈՒԹՅՈՒՆ</b>\n\n"
            "Համառոտ նկարագրեք, թե ինչու եք դա ուզում։\n\n"
            "Օրինակ՝\n"
            "<i>Ուզում եմ ամռանը դառնալ backend-ծրագրավորող</i>\n\n"
            "Կամ սեղմեք «Բաց թողնել»։"
        ),
        "goals.description_label": "📝 Նկարագրություն",
        "goals.new_description": "✏️ <b>ՆՈՐ ՆԿԱՐԱԳՐՈՒԹՅՈՒՆ</b>",
        "goals.enter_new_description": "Գրեք նոր նկարագրություն։",
        "goals.edit_description": "📝 Նկարագրություն",

        "goals.enter_result": (
            "🎯 <b>Ի՞ՆՉ ԱՐԴՅՈՒՆՔ ԵՔ ՈՒԶՈՒՄ</b>\n\n"
            "Համառոտ և կոնկրետ նկարագրեք, թե ինչ պետք է "
            "ստացվի վերջում։\n\n"
            "Օրինակ՝\n"
            "<i>Վազել 10 կմ առանց կանգ առնելու</i>\n"
            "<i>IELTS-ը հանձնել 7.0-ով</i>\n"
            "<i>Գրել 30 000 բառ վեպ</i>\n\n"
            "Կամ սեղմեք «Բաց թողնել»։"
        ),
        "goals.result_label": "🎯 Արդյունք",
        "goals.new_result": "✏️ <b>ՆՈՐ ԱՐԴՅՈՒՆՔ</b>",
        "goals.enter_new_result": "Նկարագրեք նոր արդյունքը։",
        "goals.edit_result": "🎯 Արդյունք",

        "goals.editing": "✏️ <b>ԽՄԲԱԳՐՈՒՄ</b>",
        "goals.what_edit": "Ի՞նչ եք ցանկանում փոխել։",
        "goals.new_title": "✏️ <b>ՆՈՐ ԱՆՎԱՆՈՒՄ</b>",
        "goals.enter_new_title": "Գրեք նպատակի նոր անվանումը։",
        "goals.new_duration": "⏱ <b>ՆՈՐ ՏԵՎՈՂՈՒԹՅՈՒՆ</b>",
        "goals.choose_new_duration": "Ընտրեք նոր տևողությունը։",

        "goals.started": "🚀 <b>ՆՊԱՏԱԿԸ ՍԿՍՎԵՑ</b>",
        "goals.first_step_wait": "🔥 Առաջին քայլը սպասում է ձեզ։",
        "goals.remember_cancel": (
            "Հիշեք․ նպատակը կարող եք չեղարկել միայն "
            "առաջին 72 ժամվա ընթացքում։"
        ),

        "goals.insufficient_kick": "❌ <b>KICK-Ը ԲԱՎԱՐԱՐ ՉԷ</b>",
        "goals.need_kick": "Այս նպատակի համար անհրաժեշտ է",
        "goals.data_lost": "Նպատակի տվյալները կորել են։",
        "goals.creation_cancelled": "❌ <b>ՆՊԱՏԱԿԻ ՍՏԵՂԾՈՒՄԸ ՉԵՂԱՐԿՎԵՑ</b>",
        "goals.can_create_again": "Դուք կարող եք ցանկացած պահի նոր նպատակ ստեղծել։",
        "goals.active_not_found": "Ակտիվ նպատակը չի գտնվել։",

        "goals.status_active": "🟢 Ակտիվ",
        "goals.status_completed": "🏆 Ավարտված",
        "goals.status_cancelled": "❌ Չեղարկված",
        "goals.status_failed": "💀 Ձախողված",

        "goals.progress": "📈 Առաջընթաց",
        "goals.completed": "✅ Կատարված",
        "goals.frozen": "🔒 Սառեցված",
        "goals.cancel_available": "🗑 Չեղարկումը հասանելի է ևս",
        "goals.cancel_unavailable": "🔒 <b>Չեղարկումն անհասանելի է</b>",

        "goals.step_not_found": "Այսօրվա քայլը չի գտնվել։",
        "goals.step_already_done": "Այսօրվա քայլն արդեն կատարված է։ ✅",
        "goals.first_step_unavailable": (
            "⏳ Առաջին քայլը դեռ հասանելի չէ։\n\n"
            "Փորձեք"
        ),

        "goals.completed_title": "🏆 <b>ՆՊԱՏԱԿԸ ԱՎԱՐՏՎԵՑ</b>",
        "goals.all_steps_done": "🔥 Բոլոր քայլերը կատարված են։",
        "goals.step_reward": "🪙 Պարգև",
        "goals.xp": "⚡ XP",
        "goals.step_completed": "✅ <b>ՔԱՅԼԸ ԿԱՏԱՐՎԵՑ</b>",
        "goals.day": "📅 Օր",
        "goals.level_up": "🎉 <b>LEVEL UP!</b>",
        "goals.new_level": "🏆 Նոր մակարդակ",

        "goals.steps": "📋 <b>ՆՊԱՏԱԿԻ ՔԱՅԼԵՐԸ</b>",
        "goals.day_word": "Օր",

        "goals.cancel_confirm": "🗑 <b>ՉԵՂԱՐԿԵ՞Լ ՆՊԱՏԱԿԸ</b>",
        "goals.returned": "🔒 Կվերադարձվի",
        "goals.cancel_info": "Նպատակը կչեղարկվի և այլևս ակտիվ չի համարվի։",
        "goals.cancel_unavailable_title": "🔒 <b>ՉԵՂԱՐԿՈՒՄՆ ԱՆՀԱՍԱՆԵԼԻ Է</b>",
        "goals.cancel_72_passed": (
            "Նպատակի ստեղծումից անցել է 72 ժամ։\n\n"
            "Այժմ կարող եք միայն շարունակել նպատակը։"
        ),
        "goals.too_late": "🔒 <b>ՇԱՏ ՈՒՇ Է</b>",
        "goals.too_late_text": "72 ժամը արդեն անցել է։\n\nKICK-ը մնում է սառեցված։",
        "goals.balance_error": "❌ <b>ՀԱՇՎԵԿՇՌԻ ՍԽԱԼ</b>",
        "goals.balance_error_text": (
            "Սառեցված KICK-ի քանակը չի համապատասխանում նպատակին։"
        ),
        "goals.cancelled": "🗑 <b>ՆՊԱՏԱԿԸ ՉԵՂԱՐԿՎԵՑ</b>",
        "goals.refunded": "🪙 Վերադարձվել է",
        "goals.available": "🪙 Հասանելի",
        "goals.in_goals": "🔒 Նպատակներում",
        "goals.continue": "Շարունակենք։ 💪",
        "goals.already_cancelled": "Նպատակն արդեն չեղարկված է կամ չի գտնվել։",

        "goals.heatmap_title": "📅 <b>ԱՌԱՋԸՆԹԱՑԻ ԳՈՏԻ</b>",
        "goals.heatmap_done": "կատարված",
        "goals.heatmap_missed": "բաց թողնված",
        "goals.heatmap_pending": "առաջիկա",

        "goals.note_title": "📝 <b>Ի՞ՆՉ ԱՐԵՔ</b>",
        "goals.note_hint": (
            "Նկարագրեք, թե ինչ արեցիք այսօր։\n\n"
            "Օրինակ՝\n"
            "<i>Վազեցի 5 կմ 28 րոպեում</i>"
        ),
        "goals.note_skip": "⏭ Բաց թողնել",
        "goals.note_saved": "✅ Գրանցվեց!",

        "reminder.regular_title": "⏰ Հիշեցում",
        "reminder.regular_body": "Այսօրվա քայլը դեռ կատարված չէ։ Հասցրե՛ք մինչև օրվա ավարտը։",
        "reminder.warning_title": "⚠️ Ուշադրություն",
        "reminder.warning_body": (
            "Դուք բաց թողեցիք մեկ օր։\n\n"
            "Եթե այսօր չկատարեք քայլը, նպատակը կփակվի "
            "և կհամարվի չկատարված։ KICK-ը չի վերադարձվի։"
        ),
        "goal_failed.title": "💀 ՆՊԱՏԱԿԸ ՁԱԽՈՂՎԵՑ",
        "goal_failed.body": (
            "Դուք բաց թողեցիք 2 օր անընդմեջ — նպատակը փակվեց որպես չկատարված։\n\n"
            "🔥 Մի՛ հանձնվեք — ստեղծեք նոր նպատակ և փորձե՛ք կրկին։"
        ),
        "goals.missed_warning_1": "⚠️ 1 բացթողում — հաջորդը կփակի նպատակը!",
        "goals.missed_warning_2": "💀 2 բացթողում անընդմեջ — նպատակը ձախողվեց",

        "ach.title": "🏆 <b>ՁԵՌՔԲԵՐՈՒՄՆԵՐ</b>",
        "ach.unlocked": "✅ Ստացված",
        "ach.locked": "🔒 Փակ",
        "ach.new_title": "🎉 ՆՈՐ ՁԵՌՔԲԵՐՈՒՄ!",
        "ach.profile_button": "🏆 Ձեռքբերումներ",

        # ---------- CHALLENGES ----------
        "ch.first_step_unavailable": "⏳ Առաջին քայլը դեռ հասանելի չէ։\n\nՓորձեք",

        "ch.title": "⚔️ <b>ՉԵԼԵՆՋՆԵՐ</b>",
        "ch.subtitle": (
            "Մրցեք այլ խաղացողների հետ, "
            "կատարեք նպատակները և վաստակեք KICK։\n\n"
            "Ընտրեք գործողություն։"
        ),
        "ch.find_opponent": "⚔️ <b>Մրցակցի որոնում</b>",
        "ch.choose_opponent": "⚔️ <b>Մրցակցի ընտրություն</b>",
        "ch.no_players": "Դեռ այլ խաղացողներ չկան։",
        "ch.pick_player": "Ընտրեք խաղացողին, ում ցանկանում եք մարտահրավեր նետել։",
        "ch.opponent_not_found": "Խաղացողը չի գտնվել։",
        "ch.insufficient_kick": (
            "⚠️ <b>KICK-ը բավարար չէ</b>\n\n"
            "Challenge-ի համար անհրաժեշտ է <b>{stake} KICK</b>։\n\n"
            "Ձեր հաշվեկշիռը՝ <b>{balance} KICK</b>"
        ),
        "ch.confirm_title": "⚔️ <b>CHALLENGE-Ի ՀԱՍՏԱՏՈՒՄ</b>",
        "ch.goal": "🎯 Նպատակ",
        "ch.opponent": "👤 Մրցակից",
        "ch.stake": "🪙 Խաղադրույք",
        "ch.winner_gets": "🏆 Հաղթողը ստանում է",
        "ch.frozen_notice": "Մարտահրավերն ուղարկելուց հետո խաղադրույքը կսառեցվի։",

        "ch.sent_title": "⚔️ <b>CHALLENGE-Ը ՈՒՂԱՐԿՎԵՑ</b>",
        "ch.await_accept": "⏳ Սպասում ենք ընդունմանը։",

        "ch.incoming_title": "⚔️ <b>ՁԵԶ ՄԱՐՏԱՀՐԱՎԵՐ ՆԵՏԵՑԻՆ!</b>",
        "ch.player": "👤 Խաղացող",
        "ch.duration_label": "⏱ Տևողություն",
        "ch.accept_hint": "Ընդունեք մարտահրավերը մրցույթը սկսելու համար։",
        "ch.already_exists": "Challenge-ն արդեն գոյություն ունի։",
        "ch.not_found": "Challenge-ը չի գտնվել։",
        "ch.not_for_you": "Այս Challenge-ը ձեզ համար չէ։",
        "ch.not_yours": "Սա ձեր Challenge-ը չէ։",
        "ch.already_processed": "Challenge-ն արդեն մշակված է։",

        "ch.accepted_title": "⚔️ <b>CHALLENGE-Ը ԸՆԴՈՒՆՎԵՑ!</b>",
        "ch.started": "🔥 Մրցույթը սկսվեց!",
        "ch.creator_not_found": "Challenge-ի ստեղծողը չի գտնվել։",
        "ch.your_accepted": "⚔️ <b>ՁԵՐ CHALLENGE-Ը ԸՆԴՈՒՆՎԵՑ!</b>",

        "ch.declined_title": "❌ <b>CHALLENGE-Ը ՄԵՐԺՎԵՑ</b>",
        "ch.you_declined": "Դուք մերժեցիք այս մարտահրավերը։",
        "ch.opponent_declined_your": (
            "Մրցակիցը մերժեց ձեր մարտահրավերը։\n\n"
            "🪙 {stake} KICK-ը վերադարձվեց։"
        ),

        "ch.active_title": "⚔️ <b>ԱԿՏԻՎ CHALLENGE</b>",
        "ch.pending_title": "⚔️ <b>CHALLENGE</b>",
        "ch.creator": "👤 Ստեղծող",
        "ch.opponent_short": "⚔️ Մրցակից",
        "ch.pending_wait": "⏳ Սպասում է ընդունմանը։",
        "ch.remaining": "⏳ Մնացել է",
        "ch.time_up": "⏳ <b>Ժամանակը սպառվեց</b>",
        "ch.bank": "🪙 Բանկ",
        "ch.you_ahead": "🔥 <b>Դուք առաջ եք!</b>",
        "ch.opponent_ahead": "⚔️ <b>Մրցակիցը առաջ է!</b>",
        "ch.draw_now": "🤝 <b>Հիմա ոչ-ոքի է!</b>",
        "ch.no_access": "Դուք մուտք չունեք այս Challenge-ին։",
        "ch.not_active": "Challenge-ն այլևս ակտիվ չէ։",
        "ch.time_expired": "Challenge-ի ժամանակը սպառվել է։",

        "ch.finished_title": "🏁 <b>CHALLENGE-Ը ԱՎԱՐՏՎԵՑ</b>",
        "ch.you_win": "🏆 <b>ԴՈՒՔ ՀԱՂԹԵՑԻՔ!</b>",
        "ch.you_lose": "❌ <b>ԴՈՒՔ ՊԱՐՏՎԵՑԻՔ</b>",
        "ch.draw": "🤝 <b>ՈՉ-ՈՔԻ</b>",

        "ch.today_done": "✅ <b>Այսօրվա քայլը կատարված է!</b>",
        "ch.your_progress": "Ձեր առաջընթացը",
        "ch.keep_going": "Շարունակեք վաղը! 🔥",
        "ch.step_already": "Այսօրվա քայլն արդեն կատարված է։",
        "ch.all_steps_done": "Բոլոր քայլերն արդեն կատարված են։",
        "ch.step_done_alert": "Քայլը կատարված է!",
        "ch.finished_alert": "Challenge-ը ավարտվեց!",

        "ch.win_notification": (
            "🏆 <b>ԴՈՒՔ ՀԱՂԹԵՑԻՔ!</b>\n\n"
            "⚔️ Challenge-ը ավարտվեց։\n\n"
            "🎯 Առաջընթաց՝ <b>{progress}</b>\n\n"
            "🪙 Դուք ստացաք՝ <b>{reward} KICK</b>!"
        ),
        "ch.lose_notification": (
            "❌ <b>CHALLENGE-Ը ԱՎԱՐՏՎԵՑ</b>\n\n"
            "Այս անգամ հաղթեց մրցակիցը։\n\n"
            "🔥 Մի՛ կանգնեք։"
        ),
        "ch.draw_notification": (
            "🤝 <b>ՈՉ-ՈՔԻ!</b>\n\n"
            "Երկու խաղացողներն էլ ցույց տվեցին նույն արդյունքը։\n\n"
            "🪙 Ձեզ վերադարձվեց՝ <b>{stake} KICK</b>"
        ),

        "ch.history_title": "📜 <b>CHALLENGE-Ի ՊԱՏՄՈՒԹՅՈՒՆ</b>",
        "ch.history_empty": "Պատմությունը դատարկ է։",
        "ch.status_win": "🏆 Հաղթանակ",
        "ch.status_lose": "❌ Պարտություն",
        "ch.status_draw": "🤝 Ոչ-ոքի",
        "ch.status_declined": "❌ Մերժված",
        "ch.status_expired": "⏰ Սպառված",
        "ch.status_active": "⏳ Ակտիվ",
        "ch.deleted_goal": "Ջնջված նպատակ",

        "ch.create_title": "⚔️ <b>Ստեղծել Challenge</b>",
        "ch.no_active_goals": "Դուք ակտիվ նպատակներ չունեք։\n\nՆախ ստեղծեք նպատակ։",
        "ch.pick_goal": "Ընտրեք նպատակը, որի հիման վրա կստեղծեք Challenge-ը։",
        "ch.pick_opponent_title": "⚔️ <b>ԸՆՏՐԵՔ ՄՐՑԱԿՑԻ</b>",
        "ch.whom": "Ու՞մ նետել մարտահրավեր։",

        "ch.filter_category": "🏷 <b>Ընտրեք կարգը</b>",
        "ch.filter_all": "🔷 Բոլոր կարգերը",
        "ch.goal_category": "🏷 Կարգ",
        "ch.no_opponents_category": "Այս կարգում խաղացողներ չկան։",

        "profile.title": "👤 <b>KICK ՊՐՈՖԻԼ</b>",
        "profile.balance_title": "💰 <b>ՀԱՇՎԵԿՇԻՌ</b>",
        "profile.available": "🪙 Հասանելի",
        "profile.in_goals": "🔒 Նպատակներում",
        "profile.progress_title": "📊 <b>ԱՌԱՋԸՆԹԱՑ</b>",
        "profile.level": "🏆 Մակարդակ",
        "profile.xp": "⚡ XP",
        "profile.score": "⭐ SCORE",
        "profile.streak_title": "🔥 <b>STREAK</b>",
        "profile.streak_now": "🔥 Ներկա",
        "profile.streak_best": "🏅 Ռեկորդ",
        "profile.goals_title": "🎯 <b>ՆՊԱՏԱԿՆԵՐ</b>",
        "profile.active": "🎯 Ակտիվ",
        "profile.completed": "🏆 Ավարտված",
        "profile.cancelled": "❌ Չեղարկված",
        "profile.total": "📈 Ընդամենը ստեղծված",
        "profile.user": "Օգտատեր",
        "profile.days_short": "օր",

        "rating.title": "🏆 <b>KICK LEADERBOARD</b>",
        "rating.top_players": "👑 <b>TOP PLAYERS</b>",
        "rating.your_result": "👤 <b>ՁԵՐ ԱՐԴՅՈՒՆՔԸ</b>",
        "rating.place": "🏆 Տեղ",
        "rating.level": "🏆 Մակարդակ",
        "rating.streak_label": "🔥 Streak",
        "rating.next_opponent": "⚔️ <b>ՀԱՋՈՐԴ ՄՐՑԱԿԻՑԸ</b>",
        "rating.to_him": "🎯 Նրանից",
        "rating.at_top": (
            "👑 <b>ԴՈՒՔ ԳԱԳԱԹԻՆ ԵՔ!</b>\n\n"
            "Ձեզնից վեր ոչ ոք չկա։"
        ),
        "rating.path_top10": "🎯 <b>ՃԱՆԱՊԱՐՀ ԴԵՊԻ TOP 10</b>",
        "rating.to_top10": "⬆️ Մինչև TOP 10",
        "rating.keep_going": "🔥 Շարունակեք կատարել նպատակները!",
        "rating.you_in_top10": "🔥 <b>ԴՈՒՔ TOP 10-ՈՒՄ ԵՔ!</b>",
        "rating.you_in_top10_hint": "Մի՛ կանգնեք — հաջորդ դիրքը մոտ է։ 🚀",
        "rating.metric_streak": "🔥 STREAK",
        "rating.metric_score": "⭐ SCORE",
        "rating.metric_xp": "⚡ XP",
        "rating.days_short": "օր",

        "settings.title": "⚙️ <b>ԿԱՐԳԱՎՈՐՈՒՄՆԵՐ</b>",
        "settings.choose": "Ի՞նչ եք ցանկանում կարգավորել։",
        "settings.notifications": "🔔 Ծանուցումներ",
        "settings.language": "🌐 Լեզու",
        "settings.data": "🗑 Տվյալներ",
        "settings.back": "🔙 Հետ",
        "settings.main_menu": "🏠 Գլխավոր մենյու",
        "settings.notifications_title": "🔔 <b>ԾԱՆՈՒՑՈՒՄՆԵՐ</b>",
        "settings.goal_notifications": "🎯 Նպատակներ",
        "settings.challenge_notifications": "⚔️ Չելենջներ",
        "settings.achievement_notifications": "🏆 Ձեռքբերումներ",
        "settings.choose_language": "🌐 <b>ԸՆՏՐԵՔ ԼԵԶՈՒ</b>",
        "settings.language_changed": "✅ Լեզուն փոխվեց։",
        "settings.data_title": "🗑 <b>ՏՎՅԱԼՆԵՐԻ ԿԱՌԱՎԱՐՈՒՄ</b>",
        "settings.data_description": "Ընտրեք գործողություն։",
        "settings.delete_goals": "🗑 Ջնջել բոլոր նպատակները",
        "settings.reset_progress": "🔄 Վերականգնել առաջընթացը",
        "settings.delete_account": "❌ Ջնջել հաշիվը",
        "settings.confirm_delete": "✅ Ջնջել",
        "settings.cancel": "❌ Չեղարկել",
        "settings.delete_goals_warning": (
            "⚠️ <b>ՋՆՋԵ՞Լ ԲՈԼՈՐ ՆՊԱՏԱԿՆԵՐԸ</b>\n\n"
            "Բոլոր նպատակները և կապված չելենջները կջնջվեն։\n"
            "Գործողությունն անշրջելի է։"
        ),
        "settings.confirm_delete_goals": "✅ Այո, ջնջել",
        "settings.reset_progress_warning": (
            "⚠️ <b>ՎԵՐԱԿԱՆԳՆԵ՞Լ ԱՌԱՋԸՆԹԱՑԸ</b>\n\n"
            "XP-ն, մակարդակը, score-ը և streak-ը կվերականգնվեն։"
        ),
        "settings.confirm_reset_progress": "✅ Այո, վերականգնել",
        "settings.goals_deleted": "✅ Բոլոր նպատակները ջնջվեցին։",
        "settings.progress_reset": "✅ Առաջընթացը վերականգնվեց։",
        "settings.main_menu_text": "🏠 Գլխավոր մենյու",
    },
}


def t(language: str, key: str, **kwargs) -> str:
    """Получить перевод. Если ключа нет — вернёт ключ."""
    language = language if language in TEXTS else "ru"
    text = TEXTS[language].get(key)

    if text is None:
        text = TEXTS["ru"].get(key, key)

    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text

    return text