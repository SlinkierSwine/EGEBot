from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Предметы'),
        KeyboardButton(text='Отзывы')
    ],
    [
        KeyboardButton(text='FAQ'),
        KeyboardButton(text='Вакансии')
    ]
], resize_keyboard=True)
