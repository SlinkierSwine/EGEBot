from aiogram.utils import executor

from loader import dp, bot, db

import middleware, handlers


async def on_startup(dp):
    await db.create_tables()


async def on_shutdown(dp):
    await bot.close()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
