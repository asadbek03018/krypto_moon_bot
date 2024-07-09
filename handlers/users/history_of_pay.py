from aiogram import Router, types, F
from loader import db, bot
from aiogram.filters import Command
from datetime import datetime
from keyboards.inline import menu
from loader import db

router = Router()

@router.message(F.text == "🟢Status (o'tkazmalar tarixi)")
async def history_payments_user(message: types.Message):
    db.create_table_payments()

    get_history = db.get_history_payments_telegram_id(user_id=message.from_user.id)
    if get_history:
        for history in get_history:
            status_flag = ''
            if history[10] == None:
                status_flag = "🔃Tekshirilmoqda..."
            elif history[10] == False:
                status_flag = "⛔Tranzaksiya amalga oshirilmagan"
            elif history[10] == True:
                status_flag = "✅Tranzaksiya muvaffiqiyatli amalga oshirilgan"

            pay_flag = ''
            if history[11] == None:
                pay_flag = "🔃Kutilmoqda..."
            elif history[11] == False:
                pay_flag = "❌Admin to'lovni rad etdi!"
            elif history[11] == True:
                pay_flag = "✅Admin to'lovni amalga oshirdi!"

            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"🆔O'tkazma ID: {history[2]}\n"
                f"💲O'tkazma miqdori {history[5]}\n"
                f"💰O'tkazma valyutasi: {history[4]}\n"
                f"⏲Tranzaksiya sanasi: {history[12]}\n"
                f"💳Tranzaksiya amalga oshirilgan karta: {history[7]}\n"
                f"💱To'lov: {pay_flag}\n"
                f"🟢Status: {status_flag}\n"


            )
    else:
        await message.answer(
            text="❌Sizda hech qanday o'tkazmalar mavjud emas!"
        )
