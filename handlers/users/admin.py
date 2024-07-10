import logging
import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_widgets.pagination import KeyboardPaginator
from datetime import datetime
from loader import db, bot
from keyboards.inline.buttons import are_you_sure_markup
from states.test import AdminState, AddCoin, Update_CoinNarx, SendMessageToUser
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.pgtoexcel import export_to_excel
from aiogram import F
from keyboards.inline.menu import  zakaslar, menu_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(Command('allusers'), IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    try:

        file_path = f"data/users_list.xlsx" #Tayyor
        await export_to_excel(data=users, headings=['ID', 'First_name', 'Last_name', 'Username', 'Telegram ID', 'Added_at', 'CREDIT CARD', 'CREDIT CARD PLACEHOLDER', 'CREDIT CARD DATE'], filepath=file_path)

        await message.answer_document(types.input_file.FSInputFile(file_path))
    except:
        await message.answer("😢Fayl jo'natishda xatolik yuz berdi. Yoki timeout error!")



@router.message(Command('allpayments'), IsBotAdminFilter(ADMINS))
async def get_all_payments(message: types.Message):
    payments = db.select_all_payments()
    try:
        file_path = f"data/payments_list.xlsx"
        await export_to_excel(data=payments, headings=["id", "user_id", "payments_id", "first_name", "coin_type", "coin_amount", "username", "credit_card", "credit_card_placeholder", "credit_card_exp_date", "status", "payed", "created_at"], filepath=file_path)
        await message.answer_document(types.input_file.FSInputFile(file_path))
    except:
        await message.answer("😢Fayl jo'natishda xatolik yuz berdi. Yoki timeout error!")


@router.callback_query(F.data == "home", IsBotAdminFilter(ADMINS))
async def go_to_home(call: types.CallbackQuery):
    await call.answer("🏠Menyuni boshiga qaytildi")
    await bot.send_message(chat_id=call.from_user.id, text="Assalomu alaykum Admin👋 Menu Qismi 🏠", reply_markup=menu_admin.as_markup())


@router.message(Command('menu'), IsBotAdminFilter(ADMINS))
async def menu_command(message: types.Message):
    await message.answer("Assalomu alaykum Admin👋 Menu Qismi 🏠", reply_markup=menu_admin.as_markup())



@router.message(F.text == "Reklama yuborish📬", IsBotAdminFilter(ADMINS))
async def ask_ad_content(message: types.Message, state: FSMContext):
    await message.answer("📩Reklama uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)


@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
async def send_ad_to_users(message: types.Message, state: FSMContext):
    users = db.select_all_users()
    count = 0
    for user in users:
        user_id = user[4]
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
    await state.clear()



@router.message(F.text == "Foydalanuvchiga xabar yuborish📤", IsBotAdminFilter(ADMINS))
async def get_user_id(message: types.Message, state: FSMContext):
    await message.answer("🆔Foydalanuvchi ID yozing: ")
    await state.set_state(SendMessageToUser.user_id)

@router.message(SendMessageToUser.user_id, IsBotAdminFilter(ADMINS))
async def sending_mesage(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Xabaringizni yozing📤")
    await state.set_state(SendMessageToUser.message)

@router.message(SendMessageToUser.message, IsBotAdminFilter(ADMINS))
async def done(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)

    data = await state.get_data()
    user_id = int(data.get('user_id'))
    user_message = data.get('message')
    await bot.send_message(chat_id=user_id, text=user_message)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Xabaringiz foydalanuvchiga yuborildi✅")
    await state.clear()


@router.message(F.text == "Narxlarni o'zgartirish✏", IsBotAdminFilter(ADMINS))
async def update_price(message: types.Message):
    db.create_table_coins()
    valyutalar = []
    for valyuta in db.get_all_coins():
        valyutalar.append(valyuta[1])

    buttons = [

        InlineKeyboardButton(text=f"{i}", callback_data=f"valyuta:{i}")

        for i in valyutalar

    ]
    buttons.append(InlineKeyboardButton(text='🏠Asosiy menu', callback_data='home'))

    paginator = KeyboardPaginator(
        router=router,
        data=buttons,
        per_page=20,
        per_row=2
    )

    await message.answer(f"💸Hozirgi mavjud bazadagi valyutalar: \n",
                         reply_markup=paginator.as_markup())



@router.callback_query(lambda callback_data:callback_data.data.startswith("valyuta:"))
async def get_valyuta_one(callback_data: types.CallbackQuery, state: FSMContext):
                await callback_data.message.edit_reply_markup()

                valyuta = callback_data.data.split("valyuta:")[-1]
                data = db.get_valyuta_name(name=valyuta)
                status_flag = ''
                if data[3] == True:
                    status_flag = "✅Valyuta sotuvda!"
                else:
                    status_flag = "❌Valyuta sotuvda emas!"


                valyuta_inline = [
                    [
                        InlineKeyboardButton(text="✏Nomini o'zgartirish", callback_data=f"update_name_valyuta:{data[1]}")
                    ],
                    [
                        InlineKeyboardButton(text="🔢Narxini o'zgartirish", callback_data=f"update_narx_valyuta: {data[1]}")
                    ],
                    [
                        InlineKeyboardButton(text="🟢Statusini o'zgartirish", callback_data=f"update_status_valyuta:{data[1]}")
                    ],
                    [
                        InlineKeyboardButton(text="🗑Valyutani o'chirish", callback_data=f"delete_valyuta: {data[1]}")
                    ]
                ]
                valyuta_inline_markup = InlineKeyboardMarkup(inline_keyboard=valyuta_inline)
                await bot.send_message(chat_id=callback_data.from_user.id,
                                       text=f"💲Valyuta nomi: {data[1]}\n"
                                            f"🔢Valyuta narxi: {data[2]}\n"
                                            f"🟢Status: {status_flag}\n"
                                            f"📅Updated at: {data[4]}",
                                       reply_markup=valyuta_inline_markup)

                # msg =
                # print(none_status_zakas_number)
                # global get_zakas



@router.callback_query(lambda callback_data:callback_data.data.startswith("delete_valyuta:"))
async def get_valyuta_one_delete(callback_data: types.CallbackQuery, state: FSMContext):
                await callback_data.message.edit_reply_markup()

                valyuta = callback_data.data.split("delete_valyuta:")[-1]
                data = db.get_valyuta_name(name=valyuta)
                try:
                    db.delete_coin(name=data[1])
                    await callback_data.answer(text="✅Valyuta muvaffiqiyatli o'chirildi!")
                except:
                    await callback_data.answer(text="❌Xatolik yuz berdi!")




@router.callback_query(lambda callback_data:callback_data.data.startswith("update_narx_valyuta:"))
async def get_valyuta_one_update(callback_data: types.CallbackQuery, state: FSMContext):
                await callback_data.message.edit_reply_markup()
                global data
                valyuta = callback_data.data.split("update_narx_valyuta:")[-1]
                data = db.get_valyuta_name(name=valyuta)
                await bot.send_message(chat_id=callback_data.from_user.id, text="✏Valyuta yangi qiymati")
                await state.set_state(Update_CoinNarx.narx)
@router.message(Update_CoinNarx.narx)
async def update_narx_valyuta(message: types.Message, state: FSMContext):
    await state.update_data(narx=message.text)
    now = datetime.now()
    main_data = await state.get_data()
    db.update_coin_narx(name = data[1], narx=main_data.get('narx'), updated_at=now)
    await message.answer(text="✅Qiymatlar muvaffiqiyatli saqlandi!")





@router.message(F.text == "➕Valyuta qo'shish")
async def add_valyuta(message: types.Message, state: FSMContext):
    db.create_table_coins()
    await bot.send_message(chat_id=message.from_user.id, text="✏Valyuta nomi: ")
    await state.set_state(AddCoin.name)


@router.message(AddCoin.name)
async def post_name_for_coin(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="🔢Valyutani hozirgi bahosi: ")
    await state.set_state(AddCoin.price)

@router.message(AddCoin.price)
async def post_price_for_coin(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer(text="🔃Hozir sotuvdami", reply_markup=are_you_sure_markup)
    await state.set_state(AdminState.yes_or_no)

    @router.callback_query(AdminState.yes_or_no, IsBotAdminFilter(ADMINS))
    async def ask_price_sell(call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        msg_id = data.get('msg_id')
        if call.data == 'yes':
            name = data.get('name')
            price = data.get('price')
            sell_now = True
            updated_at = datetime.now()
            db.add_coin(name, price, sell_now, updated_at)
            await call.answer(text="✅Valyuta muvaffiqiyatli saqlandi!", show_alert=True)

            await state.clear()
        elif call.data == 'no':
            name = data.get('name')
            price = data.get('price')
            sell_now = False
            updated_at = datetime.now()
            db.add_coin(name, price, sell_now, updated_at)
            await call.answer(text="✅Valyuta muvaffiqiyatli saqlandi!", show_alert=True)

            await state.clear()



########################## Zakaslar bo'limi ############################################

@router.message(F.text == "🛒Zakaslar", IsBotAdminFilter(ADMINS))
async def get_zakaslar(message: types.Message):
    db.create_table_payments()
    await message.answer("Bu yerda zakaslar tekshirilgan va tekshirilmagan hollarga bo'linadi.",
                         reply_markup=zakaslar.as_markup())


@router.message(F.text == "🟢Statusi tekshirilmagan zakaslar", IsBotAdminFilter(ADMINS))
async def status_none_zakaslar(call: types.CallbackQuery):
    zakas_ids = []
    for zakas in db.get_payments_status_none():
        zakas_ids.append(zakas[2])

    buttons = [

        InlineKeyboardButton(text=f"Zakas - #{i}", callback_data=f"none_status:{i}")

        for i in zakas_ids

    ]
    buttons.append(InlineKeyboardButton(text='🏠Asosiy menu', callback_data='home'))
    paginator = KeyboardPaginator(
        router=router,
        data=buttons,
        per_page=20,
        per_row=2
    )

    await bot.send_message(text="❌Statusi tekshirilmagan zakaslar", chat_id=call.from_user.id,
                           reply_markup=paginator.as_markup())


@router.callback_query(lambda callback_data:callback_data.data.startswith("none_status:"))
async def get_none_status(callback_data: types.CallbackQuery, state: FSMContext):
                await callback_data.message.edit_reply_markup()

                none_status_zakas_number = callback_data.data.split("none_status:")[-1]
                # print(none_status_zakas_number)
                global get_zakas

                get_zakas = db.get_zakas_payments_id(str(none_status_zakas_number))
                if get_zakas is None:
                    await bot.send_message(chat_id=callback_data.from_user.id, text="Payment not found.")
                    return

                msg = await bot.send_message(chat_id=callback_data.from_user.id, text=f"""
                        🆔Payment ID: #{get_zakas[2]}\n
                        👤User ID: {get_zakas[1]}\n
                        ℹFirst Name: {get_zakas[3]}\n
                        💰Coin Type: {get_zakas[4]}\n
                        💱Coin amount: {get_zakas[5]}\n
                        🎫Username: {get_zakas[6]}\n
                        💳Credit Card Number: {get_zakas[7]}\n
                        ◀Sending card user: {get_zakas[8]}\n
                        📅Credit Card exp date: {get_zakas[9]}
                        🔍 Foydalanuvchi sizga valyuta yuborganmi❓ 🔍

                    """, reply_markup=are_you_sure_markup)
                await state.update_data(msg_id=msg.message_id)
                await state.set_state(AdminState.yes_or_no_status)

@router.callback_query(AdminState.yes_or_no_status, IsBotAdminFilter(ADMINS))
async def ask_user_buy(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if call.data == 'yes':
        db.update_payments_status(True, get_zakas[2])
        text = "Foydalanuvchi to'lovni amalga oshirgan✅"
        await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
    elif call.data == 'no':
        db.update_payments_status(False, get_zakas[2])
        text = "Foydalanuvchi to'lovni amalga oshirmagan❌"
        await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)

    await state.clear()



@router.message(F.text == "💰To'lovi tekshirilmagan zakaslar", IsBotAdminFilter(ADMINS))
async def payed_none_zakaslar(call: types.CallbackQuery):
    zakas_ids = []
    print(zakas_ids)
    for zakas in db.get_payments_payed_none():
        # print(zakas)
        zakas_ids.append(zakas[2])

    buttons = [

        InlineKeyboardButton(text=f"Zakas - #{i}", callback_data=f"none_payed:{i}")

        for i in zakas_ids

    ]
    buttons.append(InlineKeyboardButton(text='🏠Asosiy menu', callback_data='home'))
    paginator = KeyboardPaginator(
        router=router,
        data=buttons,
        per_page=20,
        per_row=2
    )

    await bot.send_message(text="❌To'lovi tekshirilmagan zakaslar", chat_id=call.from_user.id,
                           reply_markup=paginator.as_markup())

@router.callback_query(lambda callback_data:callback_data.data.startswith("none_payed:"))
async def get_none_payed(callback_data: types.CallbackQuery, state: FSMContext):
                await callback_data.message.edit_reply_markup()

                none_payed_zakas_number = callback_data.data.split("none_payed:")[-1]
                global get_zakas
                get_zakas = db.get_zakas_payments_id(str(none_payed_zakas_number))

                msg = await bot.send_message(chat_id=callback_data.from_user.id, text=f"""
                                    🆔Payment ID: #{get_zakas[2]}\n
                                           👤User ID: {get_zakas[1]}\n
                                           ℹFirst Name: {get_zakas[3]}\n
                                           💰Coin Type: {get_zakas[4]}\n
                                           💱Coin amount: {get_zakas[5]}\n
                                           🎫Username: {get_zakas[6]}\n
                                           💳Credit Card Number: {get_zakas[7]}\n
                                           ◀Sending card user: {get_zakas[8]}\n
                                           📅Credit Card exp date: {get_zakas[9]}\n
                                           ⏲Created at: {get_zakas[12]}
                                            🔍 Siz foydalanuvchiga to'lov qilganmisiz❓ 🔍

                                    """, reply_markup=are_you_sure_markup)
                await state.update_data(msg_id=msg.message_id)
                await state.set_state(AdminState.yes_or_no_payed)

@router.callback_query(AdminState.yes_or_no_payed, IsBotAdminFilter(ADMINS))
async def ask_admin_pay_to_user(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if call.data == 'yes':
        text = "Foydalanuvchiga to'lov amalga oshirilgan✅"
        db.update_payments_payed(True, get_zakas[2])
    elif call.data == 'no':
        db.update_payments_payed(False, get_zakas[2])
        text = "To'lovdan bosh tortildi❌"
    await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)

    await state.clear()


@router.message(F.text == "✅Tekshirilgan zakaslar", IsBotAdminFilter(ADMINS))
async def checked_zakaslar(message: types.Message):
    zakas_ids = []
    for zakas in db.get_all_zakaslar():
         # Simplified condition
            zakas_ids.append(zakas[2])  # Assuming zakas[2] is the ID

    buttons = [
        InlineKeyboardButton(text=f"Zakas - #{i}", callback_data=f"checked:{i}")
        for i in zakas_ids
    ]
    buttons.append(InlineKeyboardButton(text='🏠Asosiy menu', callback_data='home'))

    paginator = KeyboardPaginator(
        router=router,
        data=buttons,
        per_page=20,
        per_row=2
    )

    await message.answer("Tekshirilgan zakaslar hammasi ✅", reply_markup=paginator.as_markup())


@router.callback_query(F.data.startswith("checked:"))
async def checked_zakaslar_one(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()

    one_checked_zakas = callback.data.split("checked:")[-1]

    get_zakas = db.get_zakas_payments_id(str(one_checked_zakas))
    status_flag_new = ''
    if get_zakas[10] == '0' or get_zakas[10] == 0:
        status_flag_new = "⛔Tranzaksiya amalga oshirilmagan"
    elif get_zakas[10] == '1' or get_zakas[10] == 1:
        status_flag_new = "✅Tranzaksiya muvaffiqiyatli amalga oshirilgan"

    payed_flag = ""
    if get_zakas[11] == "0" or get_zakas[11] == 0:
        payed_flag = "❌Admin to'lovni rad etdi!"
    elif get_zakas[11] == "1" or get_zakas[11] == 1:
        payed_flag = "✅Admin to'lovni amalga oshirdi!"


    await callback.message.answer(f"""
    🆔Payment ID: #{get_zakas[2]}
    👤User ID: {get_zakas[1]}
    ℹFirst Name: {get_zakas[3]}
    💰Coin Type: {get_zakas[4]}
    💱Coin amount: {get_zakas[5]}
    🎫Username: {get_zakas[6]}
    💳Credit Card Number: {get_zakas[7]}
    ◀Sending card user: {get_zakas[8]}
    📅Credit Card exp date: {get_zakas[9]}
    ⏲Created at: {get_zakas[12]}
    🟢Status: {status_flag_new}
    💸To'lov: {payed_flag}
    🔍✅Tekshirilgan🔍
    """)
########################### Zakaslar bo'limi tugadi ######################################

@router.message(F.text == "Bazani tozalash🧹", IsBotAdminFilter(ADMINS))
async def ask_are_you_sure(message: types.Message, state: FSMContext):
    msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?", reply_markup=are_you_sure_markup)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminState.are_you_sure)


@router.callback_query(AdminState.are_you_sure, IsBotAdminFilter(ADMINS))
async def clean_db(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if call.data == 'yes':
        db.delete_users()
        text = "Baza tozalandi!"
    elif call.data == 'no':
        text = "Bekor qilindi."
    await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
    await menu_command()
    await state.clear()

# @router.message(F.text == "Foydalanuvchiga xabar yuborish📤", IsBotAdminFilter(ADMINS))
# async def ask_user_id(message: types.Message, )