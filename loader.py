from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from utils.db.base import Database
from data.config import BOT_TOKEN, DATA_BASE

db = Database(DATA_BASE)
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
