from aiogram.types import Message

from config import REVIEWS_TEXT, REVIEWS_PARSE_MODE, FAQ_TEXT, FAQ_PARSE_MODE, \
    VACANCIES_TEXT, VACANCIES_PARSE_MODE
from keyboards.default import menu_kb
from loader import dp


@dp.message_handler(commands=['start'])
async def bot_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu_kb)


@dp.message_handler(lambda message: message.text == 'Отзывы')
async def reviews(message: Message):
    await message.answer(REVIEWS_TEXT, parse_mode=REVIEWS_PARSE_MODE)


@dp.message_handler(lambda message: message.text == 'FAQ')
async def faq(message: Message):
    await message.answer(FAQ_TEXT, parse_mode=FAQ_PARSE_MODE)


@dp.message_handler(lambda message: message.text == 'Вакансии')
async def vacancies(message: Message):
    await message.answer(VACANCIES_TEXT, parse_mode=VACANCIES_PARSE_MODE)
