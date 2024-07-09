from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from datetime import datetime
from utils.extra_datas import make_title
from keyboards.inline import menu, buttons
from keyboards.inline.menu import menu_admin


router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    """
            MARKDOWN V2                     |     HTML
    link:   [Google](https://google.com/)   |     <a href='https://google.com/'>Google</a>
    bold:   *Qalin text*                    |     <b>Qalin text</b>
    italic: _Yotiq shriftdagi text_         |     <i>Yotiq shriftdagi text</i>



                    **************     Note     **************
    Markdownda _ * [ ] ( ) ~ ` > # + - = | { } . ! belgilari to'g'ridan to'g'ri ishlatilmaydi!!!
    Bu belgilarni ishlatish uchun oldidan \ qo'yish esdan chiqmasin. Masalan  \.  ko'rinishi . belgisini ishlatish uchun yozilgan.
    """

    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    added_now = datetime.now()

    user = None


    # try:
    #
    # except Exception as error:
    #     logger.info(error)
    if telegram_id in ADMINS:
        await message.answer("Assalomu alaykum Admin👮‍♂️", reply_markup=menu_admin.as_markup(
            resize_keyboard=True
        ))

    else:

        if db.check_user_exists(telegram_id=telegram_id):

            await message.answer(f"Assalomu alaykum {make_title(full_name)}\!", parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=buttons.starting_links_markup)
            # await
            await bot.send_message(chat_id=message.from_user.id, text="🏠Asosiy menu👇", reply_markup=menu.menu.as_markup(
                resize_keyboard=True
            ))
        else:

            count = db.count_users()


            db.add_user(first_name=message.from_user.first_name, last_name=message.from_user.last_name,
                                     username=username, telegram_id=telegram_id, added_at=added_now, credit_card=None,
                                     credit_card_placeholder=None, credit_card_exp_date=None)


            await message.answer(f"Assalomu alaykum {make_title(full_name)}\! Bazadagi a'zolar soni: {count}", parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=buttons.starting_links_markup)
            # await
            await bot.send_message(chat_id=message.from_user.id, text="🏠Asosiy menu👇", reply_markup=menu.menu.as_markup(
                resize_keyboard=True
            ))

            for admin in ADMINS:
                try:
                    await bot.send_message(chat_id=admin,
                                           text=f"🆕Bazaga yangi foydalanuvchi qo'shildi\n"
                                                f"ℹFirst_name: {message.from_user.first_name}\n"
                                                f"🎫Username: {message.from_user.username}\n"
                                                f"🆔Telegram ID: {telegram_id}\n"
                                                f"⏲Qo'shilgan vaqt: {added_now}"
                                           )

                except Exception as error:
                    logger.info(f"Adminga qo'shilgan xabari yuborib bo'lmadi. Admin: {admin}. Xatolik: {error}")
    # for admin in ADMINS:
    #     try:
    #         await bot.send_message(
    #             chat_id=admin,
    #             text=msg,
    #             parse_mode=ParseMode.MARKDOWN_V2
    #         )
    #     except Exception as error:
    #         logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    #

    # await message.answer(f"Assalomu alaykum {make_title(full_name)}\!", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=buttons.starting_links_markup)
    # # await
    # await bot.send_message(chat_id=message.from_user.id, text="🏠Asosiy menu👇", reply_markup=menu.menu.as_markup())