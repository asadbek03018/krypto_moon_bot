from aiogram import Router, types, F
from aiogram.filters.command import Command

router = Router()


@router.message(F.text == "❓Yordam")
async def bot_help(message: types.Message):
    text = ("🆕Bu bot orqali krypto aktivlarni ayriboshlash va ular haqida eng so'ngi ma'lumotlarni bilib tura olasiz"
            "📑Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/history_pay - To'lovlar tarixi",
            "/me - Mening profilim",
            "/send_message - Adminga xabar",
            "/kurs - Valyuta kursi",
            "/sell - 💎Valyuta sotish",
            "👥Guruhimiz: @krypto_moon_chat"

            )
    await message.answer(text="\n".join(text))
