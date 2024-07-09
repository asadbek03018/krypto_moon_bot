from aiogram import Router, types, F
from aiogram.enums.parse_mode import ParseMode
from loader import bot
from utils.extra_datas import make_title
from keyboards.inline import menu, buttons




router = Router()

@router.message(F.text == "↩Qaytish")

async def go_to_home_menu(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"Assalomu alaykum {make_title(full_name)}\!", parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=buttons.starting_links_markup)
    # await
    await bot.send_message(chat_id=message.from_user.id, text="🏠Asosiy menu👇", reply_markup=menu.menu.as_markup(
        resize_keyboard=True
    ))
