from aiogram.filters.state import StatesGroup, State

class Message(StatesGroup):
    user_message = State()

