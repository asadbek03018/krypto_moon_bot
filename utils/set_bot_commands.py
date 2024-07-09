from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="⚡Botni ishga tushirish"),
        BotCommand(command="/help", description="❓Yordam"),
        BotCommand(command="/faq", description="📃Kerakli ma'lumotlar"),
        BotCommand(command="/admins", description="👮‍♂️Adminlar"),
        BotCommand(command="/info", description="ℹBot haqida ma'lumotlar"),


    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
