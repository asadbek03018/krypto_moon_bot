from aiogram.filters.state import StatesGroup, State

class SendMoney(StatesGroup):
    first_name = State()
    coin_amount = State()
    credit_card = State()
    credit_card_placeholder = State()
    credit_card_exp_date = State()


class NotcoinStates(StatesGroup):
    first_name = State()
    coin_amount = State()
    credit_card = State()
    credit_card_placeholder = State()

class HamsterStates(StatesGroup):
    first_name = State()
    coin_amount = State()
    credit_card = State()
    credit_card_placeholder = State()

class TapSwapStates(StatesGroup):
    first_name = State()
    coin_amount = State()
    credit_card = State()
    credit_card_placeholder = State()