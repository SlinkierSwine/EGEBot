from aiogram import Bot, Dispatcher, types

import config
from data.db.database import DataBase

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

db = DataBase(config.DATABASE_PATH)
