from aiogram.fsm.state import State, StatesGroup


class GoalStates(StatesGroup):
    waiting_for_duration = State()
    waiting_for_custom_duration = State()
    waiting_for_title = State()

    choosing_category = State()
    waiting_for_description = State()
    waiting_for_result = State()          # NEW

    preview = State()

    editing_title = State()
    editing_description = State()
    editing_result = State()              # NEW
    editing_duration = State()
    editing_custom_duration = State()

    waiting_for_step_note = State()