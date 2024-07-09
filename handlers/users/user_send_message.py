from aiogram import Router, types, F
from loader import db, bot
from datetime import datetime
from aiogram.fsm.context import FSMContext
from states.send_message import Message
from data.config import ADMINS
from aiogram.client.session.middlewares.request_logging import logger
from keyboards.inline.menu import cancel
from aiogram.filters import Command

router = Router()

@router.message(F.text == '👮‍♂️Adminga murojaat')
async def send_message_to_admin(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text="📩Xabaringizni yuboring!", reply_markup=cancel.as_markup())
    await state.set_state(Message.user_message)


@router.message(Message.user_message)
async def send_to_admin(message: types.Message, state: FSMContext):



    await state.update_data(user_message=message.text)

    msg_data = await state.get_data()

    msg = msg_data.get('user_message')

    total = (f">>>>>>>>🆔User ID: {message.from_user.id}\n"
             f"📝Username: {message.from_user.username}\n"
             f"🎫User first_name: {message.from_user.first_name}\n"
             f"🆗User last_name: {message.from_user.last_name}>>>>>>>>\n"
             f"📨Message body: {msg}")


    await message.answer("✅Xabaringiz adminlarga yetkazildi. Tez orada sizga javob berishadi!")
    await message.answer("✅")
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=total,

            )
        except Exception as error:
            logger.info(f"Adminga xabar jo'natib bo'lmadi!: {admin}. Error: {error}")
    await state.clear()

