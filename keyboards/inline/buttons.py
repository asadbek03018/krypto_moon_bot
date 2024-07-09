from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

starting_links = [
    [
        InlineKeyboardButton(text="👮‍♂️Admin", url="https://t.me/HTSWPCoin_Bu"),
        InlineKeyboardButton(text="👮‍♂️Admin2", url="https://t.me/KryptoMoonSupport"),
        InlineKeyboardButton(text="📊Kanalimiz", url="https://t.me/Crypto_UZEX")
    ]
]

starting_links_markup = InlineKeyboardMarkup(inline_keyboard=starting_links)

