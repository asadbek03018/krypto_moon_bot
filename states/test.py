from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
    yes_or_no = State()
    yes_or_no_status = State()
    yes_or_no_payed = State()
    yes_or_no_delete_account = State()

class AddCoin(StatesGroup):
    name = State()
    price = State()

class UpdateCardUser(StatesGroup):
    credit_card = State()
    credit_card_placeholder = State()

class Update_CoinNarx(StatesGroup):
    narx = State()


class SendMessageToUser(StatesGroup):
    user_id = State()
    message = State()
