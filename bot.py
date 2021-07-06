from aiogram.utils import executor

from loader import dp, bot

import middleware, handlers


async def on_shutdown(dp):
    await bot.close()

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown)
