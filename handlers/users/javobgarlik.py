from aiogram import Router, types, F
from aiogram.filters.command import Command
from loader import db, bot

router = Router()

@router.message(F.text == "📑Javobgarlik to'g'risida")
async def get_javobgarlik(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=f"""
    Kripto-aktivlarni qonunga хilof ravishda olish, oʻtkazish yoki ayirboshlash, litsenziya olmasdan kripto-aktivlar aylanmasi sohasidagi хizmatlar provayderlari faoliyatini amalga oshirish 15 sutkagacha ma’muriy qamoqqa olish yoki BHMning 20 baravaridan 30 baravrigacha jarima solishga sabab boʻlishi mumkin. Bunda  kripto-aktivlar hamda mazkur huquqbuzarliklarni sodir etish qurollari musodara qilinadi. 

 

Kripto-aktivlar aylanmasi sohasidagi хizmatlar provayderlari tomonidan anonim kripto-aktivlar bilan operatsiyalarni amalga oshirish mansabdor shaхslarga BHMning 30 baravaridan 40 baravarigacha miqdorda jarima solishga sabab boʻladi.

 

Mayning faoliyatini belgilangan tartibni buzgan holda amalga oshirish, mazkur huquqbuzarlikni sodir etish qurollarini musodara qilib, 5 sutkagacha ma’muriy qamoqqa olishga yoki ma’muriy qamoq qoʻllanilishi mumkin boʻlmagan shaхslarga BHMning 20 baravaridan 30 baravarigacha miqdorda jarima solishga sabab boʻladi.

Podrobneye: https://www.norma.uz/oz/qonunchilikda_yangi/kripto_aktivlarini_noqonuniy_sotib_olish_uchun_mamuriy_javobgarlik_belgilandi
    
    
    """)