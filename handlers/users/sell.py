from aiogram.types import Message, CallbackQuery
from keyboards.inline import menu
import random
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states.send_money import SendMoney, TapSwapStates, HamsterStates, NotcoinStates
from loader import bot, db
from datetime import datetime
from data.config import ADMINS


router = Router()

@router.message(F.text == "💱Ayriboshlash")
async def sell_valyuta(message: Message, state: FSMContext):
    await message.answer(
        "Ayriboshlamoqchi bo'lgan valyutangizni tanlang👇👇",
        reply_markup=menu.send_money.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Valyutani tanlang!"
        )
    )




################################################# Notcoin #####################################

@router.message(F.text == "💎Notcoin")
async def sell_not(message: Message, state: FSMContext):
    await message.answer("✍Ismingizni kiriting (⚠Diqqat⚠ Ism kirityotganda taxalluslar yozilmaydi):")
    await state.set_state(NotcoinStates.first_name)

@router.message(NotcoinStates.first_name)
async def get_first_name_notcoin(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("💱Notcoin miqdori (Qancha, Masalan: 13000)\n"
                         "🔗Hamyon Raqamiga koini o'tkazing: \ngdhsjkd73777382iejdjjd93877r77r")

    await state.set_state(NotcoinStates.coin_amount)

@router.message(NotcoinStates.coin_amount)
async def get_coin_amount_notcoin(message: Message, state: FSMContext):
    coin_amount = message.text
    await state.update_data(coin_amount=message.text)
    await message.answer("💳Plastik karta raqami: (⚠Diqqat⚠ Plastik kartadagi hech qanday pul o'g'rlanmaydi aksincha siz sotgan kripto-valyutaga pul tashlanadi!)\n"
                         "Plastik karta raqami misol: 8600 5805 1581 1822")

    await state.set_state(NotcoinStates.credit_card)

@router.message(NotcoinStates.credit_card)
async def get_credit_card_number_notcoin(message: Message, state: FSMContext):
    await state.update_data(credit_card=message.text)
    await message.answer("ℹPlastik karta egasining ism familyasi (⚠Diqqat⚠ Agar plastik karta egasining ism familyasi bilan mos kelmasa pul tashlab berilmaydi!)\n"
                         "Misol uchun: Karimov Karimjon")

    await state.set_state(NotcoinStates.credit_card_placeholder)

@router.message(NotcoinStates.credit_card_placeholder)
async def get_credit_card_placeholder_notcoin(message: Message, state: FSMContext):
    await state.update_data(credit_card_place_holder=message.text)
    await message.answer("📅Plastik kartaning eskirish sanasi: (⚠Diqqat⚠ Bu yerdagi ma'lumotlar hech qaerga chiqmaydi! Va har bir foydalanuvchining ma'lumotlari sir saqalandi. Bu faqat to'lov amalga oshirish maqsadida tekshiriladi.) \n"
                         "😊Bizga ishonganingiz uchun rahmat. Adminlar tez orada to'lovni amalga oshiradilar")

    send_money = await state.get_data()
    payments_id = ''.join(random.choices('0123456789', k=5))
    user_id = message.from_user.id
    first_name = send_money.get('first_name')
    coin_type = 'notcoin'
    coin_amount = send_money.get('coin_amount')
    username = message.from_user.username
    credit_card = send_money.get('credit_card')
    credit_card_placeholder = send_money.get('credit_card_placeholder')
    credit_card_exp_date = send_money.get('credit_card_exp_date')
    status = None
    payed = None
    created_at = datetime.now()
    db.create_table_payments()

    db.add_payment(user_id=int(user_id), payments_id=payments_id, first_name=first_name, coin_type=coin_type, coin_amount=coin_amount, username=username, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder, credit_card_exp_date=credit_card_exp_date, status=status, payed=payed, created_at=created_at)
    db.update_credit_card(chat_id=user_id, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder)
    total = f"""
        🆔Payment ID: #{payments_id}\n
                           👤User ID: {user_id}\n
                           ℹFirst Name: {first_name}\n
                           💰Coin Type: {coin_type}\n
                           💱Coin amount: {coin_amount}\n
                           🎫Username: {username}\n
                           💳Credit Card Number: {credit_card}\n
                           ◀Sending card user: {credit_card_placeholder}\n
                           📅Credit Card exp date: {credit_card_exp_date}
"""


    await bot.send_message(chat_id=message.from_user.id,
                           text=f"🆔Payment ID: #{payments_id}\n"
                           f"👤User ID: {user_id}\n"
                           f"ℹFirst Name: {first_name}\n"
                           f"💰Coin Type: {coin_type}\n"
                           f"💱Coin amount: {coin_amount}\n"
                           f"🎫Username: {username}\n"
                           f"💳Credit Card Number: {credit_card}\n"
                           f"◀Sending card user: {credit_card_placeholder}\n"
                           f"📅Credit Card exp date: {credit_card_exp_date}")

    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=total,

            )
        except Exception as error:
            logger.info(f"Adminga xabar jo'natib bo'lmadi!: {admin}. Error: {error}")
    await bot.send_message(chat_id=message.from_user.id, text=f"✅Admin uchun tekshirishuvga jo'natildi. Statusni tekshirishni unutmang!")

    await state.clear()


########################################## Hamster Kombat ###################################

@router.message(F.text == "🐹Hamster Kombat")
async def sell_hamster(message: Message, state: FSMContext):
    await message.answer("""✍Ismingizni kiriting (⚠Diqqat⚠ Ism kirityotganda taxalluslar yozilmaydi):""")
    await state.set_state(HamsterStates.first_name)

@router.message(HamsterStates.first_name)
async def get_first_name_hamster(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("🐹Hamster Kombat miqdori (Qancha, Masalan: 13000)\n"
                         "🔗Hamyon Raqamiga koini o'tkazing: \ngdhsjkd73777382iejdjjd93877r77r")
    await state.set_state(HamsterStates.coin_amount)

@router.message(HamsterStates.coin_amount)
async def get_coin_amount_hamster(message: Message, state: FSMContext):
    coin_amount = message.text
    await state.update_data(coin_amount=message.text)
    await message.answer("💳Plastik karta raqami: (⚠Diqqat⚠ Plastik kartadagi hech qanday pul o'g'rlanmaydi aksincha siz sotgan kripto-valyutaga pul tashlanadi!)\n"
                         "Plastik karta raqami misol: 8600 5805 1581 1822")

    await state.set_state(HamsterStates.credit_card)

@router.message(HamsterStates.credit_card)
async def get_credit_card_number_hamster(message: Message, state: FSMContext):
    await state.update_data(credit_card=message.text)
    await message.answer("ℹPlastik karta egasining ism familyasi (⚠Diqqat⚠ Agar plastik karta egasining ism familyasi bilan mos kelmasa pul tashlab berilmaydi!)\n"
                         "Misol uchun: Karimov Karimjon")

    await state.set_state(HamsterStates.credit_card_placeholder)

@router.message(HamsterStates.credit_card_placeholder)
async def get_credit_card_placeholder_hamster(message: Message, state: FSMContext):
    await state.update_data(credit_card_place_holder=message.text)
    await message.answer("📅Plastik kartaning eskirish sanasi: (⚠Diqqat⚠ Bu yerdagi ma'lumotlar hech qaerga chiqmaydi! Va har bir foydalanuvchining ma'lumotlari sir saqalandi. Bu faqat to'lov amalga oshirish maqsadida tekshiriladi.) \n"
                         "😊Bizga ishonganingiz uchun rahmat. Adminlar tez orada to'lovni amalga oshiradilar")

    send_money = await state.get_data()
    payments_id = ''.join(random.choices('0123456789', k=5))
    user_id = message.from_user.id
    first_name = send_money.get('first_name')
    coin_type = 'hamster'
    coin_amount = send_money.get('coin_amount')
    username = message.from_user.username
    credit_card = send_money.get('credit_card')
    credit_card_placeholder = send_money.get('credit_card_placeholder')
    credit_card_exp_date = send_money.get('credit_card_exp_date')
    status = None
    payed = None
    created_at = datetime.now()
    db.create_table_payments()

    db.add_payment(user_id=int(user_id), payments_id=payments_id, first_name=first_name, coin_type=coin_type, coin_amount=coin_amount, username=username, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder, credit_card_exp_date=credit_card_exp_date, status=status, payed=payed, created_at=created_at)
    db.update_credit_card(chat_id=user_id, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder)
    total = f"""
        🆔Payment ID: #{payments_id}\n
                           👤User ID: {user_id}\n
                           ℹFirst Name: {first_name}\n
                           💰Coin Type: {coin_type}\n
                           💱Coin amount: {coin_amount}\n
                           🎫Username: {username}\n
                           💳Credit Card Number: {credit_card}\n
                           ◀Sending card user: {credit_card_placeholder}\n
                           📅Credit Card exp date: {credit_card_exp_date}
"""


    await bot.send_message(chat_id=message.from_user.id,
                           text=f"🆔Payment ID: #{payments_id}\n"
                           f"👤User ID: {user_id}\n"
                           f"ℹFirst Name: {first_name}\n"
                           f"💰Coin Type: {coin_type}\n"
                           f"💱Coin amount: {coin_amount}\n"
                           f"🎫Username: {username}\n"
                           f"💳Credit Card Number: {credit_card}\n"
                           f"◀Sending card user: {credit_card_placeholder}\n"
                           f"📅Credit Card exp date: {credit_card_exp_date}")

    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=total,

            )
        except Exception as error:
            logger.info(f"Adminga xabar jo'natib bo'lmadi!: {admin}. Error: {error}")
    await bot.send_message(chat_id=message.from_user.id, text=f"✅Admin uchun tekshirishuvga jo'natildi. Statusni tekshirishni unutmang!")

    await state.clear()


####################################3 TapSwap #########################################

@router.message(F.text == "🪙TapSwap")
async def sell_tapswap(message: Message, state: FSMContext):
    await message.answer("""✍Ismingizni kiriting (⚠Diqqat⚠ Ism kirityotganda taxalluslar yozilmaydi):""")
    await state.set_state(TapSwapStates.first_name)

@router.message(TapSwapStates.first_name)
async def get_first_name_tapswap(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("🪙TapSwap miqdori (Qancha, Masalan: 13000)\n"
                         "🔗Hamyon Raqamiga koini o'tkazing: \ngdhsjkd73777382iejdjjd93877r77r")
    await state.set_state(TapSwapStates.coin_amount)

@router.message(TapSwapStates.coin_amount)
async def get_coin_amount_tapswap(message: Message, state: FSMContext):
    coin_amount = message.text
    await state.update_data(coin_amount=message.text)
    await message.answer("💳Plastik karta raqami: (⚠Diqqat⚠ Plastik kartadagi hech qanday pul o'g'rlanmaydi aksincha siz sotgan kripto-valyutaga pul tashlanadi!)\n"
                         "Plastik karta raqami misol: 8600 5805 1581 1822")

    await state.set_state(TapSwapStates.credit_card)

@router.message(TapSwapStates.credit_card)
async def get_credit_card_number_tapswap(message: Message, state: FSMContext):
    await state.update_data(credit_card=message.text)
    await message.answer("ℹPlastik karta egasining ism familyasi (⚠Diqqat⚠ Agar plastik karta egasining ism familyasi bilan mos kelmasa pul tashlab berilmaydi!)\n"
                         "Misol uchun: Karimov Karimjon")

    await state.set_state(TapSwapStates.credit_card_placeholder)

@router.message(TapSwapStates.credit_card_placeholder)
async def get_credit_card_placeholder_tapswap(message: Message, state: FSMContext):
    await state.update_data(credit_card_place_holder=message.text)
    await message.answer("📅Plastik kartaning eskirish sanasi: (⚠Diqqat⚠ Bu yerdagi ma'lumotlar hech qaerga chiqmaydi! Va har bir foydalanuvchining ma'lumotlari sir saqalandi. Bu faqat to'lov amalga oshirish maqsadida tekshiriladi.) \n"
                         "😊Bizga ishonganingiz uchun rahmat. Adminlar tez orada to'lovni amalga oshiradilar")

    send_money = await state.get_data()
    payments_id = ''.join(random.choices('0123456789', k=5))
    if db.check_payments_id_exists(payments_id=payments_id):
        payments_id = ''.join(random.choices('0123456789', k=5))




    user_id = message.from_user.id
    first_name = send_money.get('first_name')
    coin_type = 'tapswap'
    coin_amount = send_money.get('coin_amount')
    username = message.from_user.username
    credit_card = send_money.get('credit_card')
    credit_card_placeholder = send_money.get('credit_card_placeholder')
    credit_card_exp_date = send_money.get('credit_card_exp_date')
    status = None
    payed = None
    created_at = datetime.now()
    db.create_table_payments()

    db.add_payment(user_id=int(user_id), payments_id=payments_id, first_name=first_name, coin_type=coin_type, coin_amount=coin_amount, username=username, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder, credit_card_exp_date=credit_card_exp_date, status=status, payed=payed, created_at=created_at)
    db.update_credit_card(chat_id=user_id, credit_card=credit_card, credit_card_placeholder=credit_card_placeholder)
    total = f"""
        🆔Payment ID: #{payments_id}\n
                           👤User ID: {user_id}\n
                           ℹFirst Name: {first_name}\n
                           💰Coin Type: {coin_type}\n
                           💱Coin amount: {coin_amount}\n
                           🎫Username: {username}\n
                           💳Credit Card Number: {credit_card}\n
                           ◀Sending card user: {credit_card_placeholder}\n
                           📅Credit Card exp date: {credit_card_exp_date}
"""


    await bot.send_message(chat_id=message.from_user.id,
                           text=f"🆔Payment ID: #{payments_id}\n"
                           f"👤User ID: {user_id}\n"
                           f"ℹFirst Name: {first_name}\n"
                           f"💰Coin Type: {coin_type}\n"
                           f"💱Coin amount: {coin_amount}\n"
                           f"🎫Username: {username}\n"
                           f"💳Credit Card Number: {credit_card}\n"
                           f"◀Sending card user: {credit_card_placeholder}\n"
                           f"📅Credit Card exp date: {credit_card_exp_date}")

    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=total,

            )
        except Exception as error:
            logger.info(f"Adminga xabar jo'natib bo'lmadi!: {admin}. Error: {error}")
    await bot.send_message(chat_id=message.from_user.id, text=f"✅Admin uchun tekshirishuvga jo'natildi. Statusni tekshirishni unutmang!")

    await state.clear()
