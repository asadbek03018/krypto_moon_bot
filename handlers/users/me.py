from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from loader import db, bot
from datetime import datetime
from keyboards.inline import menu, buttons
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from states.test import UpdateCardUser, AdminState
router = Router()

global user


@router.message(F.text == "👤Akkuntim")
async def my_account(message: types.Message):
    telegram_id = message.from_user.id

    full_name = message.from_user.full_name
    username = message.from_user.username

    added_now = datetime.now()
    user = db.get_user_telegram_id(telegram_id=message.from_user.id)
    try:
        added_at = user[5]
        if user:
            msg = (
                f"👤Foydalanuvchi ma'lumotlari: \n"
                f"Ism: {message.from_user.first_name}\n"
                f"Familya: {message.from_user.last_name}\n"
                f"Username: {username}\n"
                f"⏲Botga qo'shilgan sana: {added_at}"
            )
        else:

            db.add_user(telegram_id=telegram_id, username=username,
                        first_name=message.from_user.first_name, last_name=message.from_user.last_name, credit_card=None,
                        credit_card_placeholder=None, credit_card_exp_date=None, added_at=added_now)
            user = db.get_user_telegram_id(telegram_id=message.from_user.id)

            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.last_name
            added_at = user[5]

            msg = (
                f"👤Foydalanuvchi ma'lumotlari: \n"
                f"Ism: {first_name}\n"
                f"Familya: {last_name}\n"
                f"Username: {username}\n"
                f"⏲Botga qo'shilgan sana: {added_at}"
            )

        await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=menu.account.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Mening akkauntim"
        ))
    except:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.last_name
        db.add_user(telegram_id=telegram_id, username=username,
                    first_name=message.from_user.first_name, last_name=message.from_user.last_name, credit_card=None,
                    credit_card_placeholder=None, credit_card_exp_date=None, added_at=added_now)
        user = db.get_user_telegram_id(telegram_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text="Yangi akkaunt yaratish✅",
            reply_markup=menu.account.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Mening akkauntim"))



@router.message(F.text == "🗑Akkuntimni bazadan o'chirish")
async def delete_my_account(message: types.Message, state: FSMContext):
    msg = await message.answer("Haqiqatdan ham akkauntingizni o'chirasizmi❓"
                         "Sizdagi barcha ma'lumotlar unutiladi🗑"
                         "Jumladan👇👇👇"
                         "Barcha o'tkazmalar❌"
                         "Saqlangan kartalar❌", reply_markup=buttons.are_you_sure_markup)

    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminState.yes_or_no_delete_account)

@router.callback_query(AdminState.yes_or_no_delete_account)
async def delete_my_account_ask(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if call.data == 'yes':
        db.delete_user(call.from_user.id)
        text = "Akkaunt o'chirildi✅"
    elif call.data == 'no':
        text = "Bekor qilindi❌"

    await call.answer(text=text)


@router.message(F.text == "💳Karta raqamni almashtirish")
async def change_card_number(message: types.Message):

    if db.is_card_number(telegram_id=message.from_user.id):
        global user
        user = db.get_user_telegram_id(
            telegram_id=message.from_user.id
        )
        card_number = [
            [
                InlineKeyboardButton(text=f"{user[6]}", callback_data=f"update:{user[6]}"),
            ],
            [
                InlineKeyboardButton(text="🗑Kartani o'chirish", callback_data=f"delete:{user[6]}")
            ],
            [
                InlineKeyboardButton(text="🏠Home", callback_data='home')
            ]
        ]
        card_number_mark = InlineKeyboardMarkup(inline_keyboard=card_number)
        await message.answer("💳Karta raqamni almashtirish",  reply_markup=card_number_mark)

    else:
        await message.answer("Sizda xali karta raqami mavjud emas❌")


@router.callback_query(lambda callback_data: callback_data.data.startswith("update:"))
async def get_update_card(callback_data: types.CallbackQuery, state: FSMContext):
                await callback_data.message.edit_reply_markup()
                global credit_card_number
                credit_card_number = callback_data.data.split("update:")[-1]
                # print(none_status_zakas_number)
                await callback_data.message.answer("✏Yangi karta raqamini kiriting: ")
                await state.set_state(UpdateCardUser.credit_card)
@router.message(UpdateCardUser.credit_card)
async def get_credit_card_number(message: types.Message, state: FSMContext):
    await state.update_data(credit_card=message.text)
    await message.answer("👤Karta egasining ismi familyasi: ")
    await state.set_state(UpdateCardUser.credit_card_placeholder)

@router.message(UpdateCardUser.credit_card_placeholder)
async def get_credit_card_full(message: types.Message, state: FSMContext):
    await state.update_data(credit_card_placeholder=message.text)
    data = await state.get_data()
    credit_card = data.get('credit_card')
    credit_card_placeholder = data.get('credit_card_placeholder')
    db.update_credit_card(chat_id=message.from_user.id, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder)
    await bot.send_message(chat_id=message.from_user.id, text="Plastik karta muvaffiqiyatli saqlandi✅")
    await state.clear()

@router.callback_query(lambda callback_data: callback_data.data.startswith("delete:"))
async def get_update_card(callback_data: types.CallbackQuery, state: FSMContext):
    await callback_data.message.edit_reply_markup()
    global credit_card_number
    credit_card_number = callback_data.data.split("delete:")[-1]
