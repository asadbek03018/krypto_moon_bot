from aiogram import Router, types, F
from aiogram.filters import Command
from loader import db
router = Router()

@router.message(F.text == '💲Valyuta kursi')
async def valyuta_kurs(message: types.Message):
    db.create_table_coins()
      # Ma'lumotlar bazasi bilan ishlovchi klassingizni yarating
    coins = db.get_all_coins()
    
    if not coins:
        await message.answer("❌Hozircha valyuta kurslari kiritilmagan.")
        return
    
    response = "💲Hozirgi valyuta kursi\n"
    for coin in coins:
        coin_status = ''
        if coin[3]:
            coin_status = "✅Hozir sotuvda ishlamoqda"
        else:
            coin_status = "❌Sotib olish mavjud emas!"

        sell_status = "✅Hozir sotuvda" if coin[3] else "❌Bizda sotib olish mavjud emas"
        response += f"ℹ{coin[1]}: 🔢{coin[2]} | 🟢{coin_status} | ⏲Yangilangan: {coin[4]}\n"
    
    await message.answer(response)