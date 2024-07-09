from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


menu_admin = ReplyKeyboardBuilder()
menu_admin.row(
    KeyboardButton(text="Foydalanuvchiga xabar yuborish📤"),
            KeyboardButton(text="🛒Zakaslar")
)

menu_admin.row(
    KeyboardButton(text="Narxlarni o'zgartirish✏"),
            KeyboardButton(text="Reklama yuborish📬")
)


menu_admin.row(
    KeyboardButton(text="Statistika📊"),
            KeyboardButton(text="Adminlarni boshqarish📝")
)

menu_admin.row(
    KeyboardButton(text="Bazani tozalash🧹"),
    KeyboardButton(text="➕Valyuta qo'shish")
)

menu = ReplyKeyboardBuilder()


menu.row(
        KeyboardButton(text="👤Akkuntim"),
                 KeyboardButton(text="📑Javobgarlik to'g'risida")
)

menu.row(
    KeyboardButton(text="💱Ayriboshlash"),
            KeyboardButton(text="❓Yordam")
)

menu.row(
    KeyboardButton(text="💰Narxlar"),
            KeyboardButton(text="💲Valyuta kursi")
)

menu.row(
    KeyboardButton(text="🟢Status (o'tkazmalar tarixi)"),
            KeyboardButton(text="👮‍♂️Adminga murojaat")
)



# edit_money_price = ReplyKeyboardBuilder()
# edit_money_price.row(
#     KeyboardButton(text="➕Valyuta qo'shish")
# )

cancel = ReplyKeyboardBuilder()
cancel.row(
    KeyboardButton(text="↩Qaytish")
)

send_money = ReplyKeyboardBuilder()
send_money.row(
    KeyboardButton(text="💎Notcoin"),
            KeyboardButton(text="🪙TapSwap"),


)

send_money.row(
    KeyboardButton(text="🐹Hamster Kombat"),
            KeyboardButton(text="↩Qaytish")
)

account = ReplyKeyboardBuilder()
account.row(
    KeyboardButton(text="💳Karta raqamni almashtirish"),


)

account.row(
    KeyboardButton(text="🗑Akkuntimni bazadan o'chirish")
)

account.row(
    KeyboardButton(text="↩Qaytish")
)

zakaslar = ReplyKeyboardBuilder()
zakaslar.row(
    KeyboardButton(text="🟢Statusi tekshirilmagan zakaslar"),
    KeyboardButton(text="💰To'lovi tekshirilmagan zakaslar")
)
zakaslar.row(
    KeyboardButton(text="✅Tekshirilgan zakaslar")
)