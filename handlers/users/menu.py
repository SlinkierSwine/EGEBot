from aiogram.types import Message

from loader import dp


@dp.message_handler(lambda message: message.text == 'Отзывы')
async def reviews(message: Message):
    await message.answer('Отзывы')


@dp.message_handler(lambda message: message.text == 'FAQ')
async def reviews(message: Message):
    await message.answer('FAQ')


@dp.message_handler(lambda message: message.text == 'Вакансии')
async def reviews(message: Message):
    await message.answer('Вакансии')
