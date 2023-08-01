from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    TaskFirst = State()
    TaskFirstLesson = State()
    TaskFirstAnswer = State()
    task_2 = State()