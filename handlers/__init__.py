from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import admin, start, help, me, history_of_pay, user_send_message, sell, go_to_home, javobgarlik, valyuta_kursi
    from .errors import error_handler


    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

    router.include_routers(admin.router, go_to_home.router, valyuta_kursi.router, javobgarlik.router, start.router, help.router,  me.router, history_of_pay.router, user_send_message.router, sell.router, error_handler.router)

    return router
