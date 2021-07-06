from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import make_callback_data
from loader import db


async def list_subjects_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=2)

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    subjects = await db.get_list_subjects()
    for subject in subjects:
        # Сформируем колбек дату, которая будет на кнопке.
        # Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject=subject[0])

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=subject[1], callback_data=callback_data)
        )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными подкатегориями, исходя из выбранной категории
async def list_courses_keyboard(subject):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)

    # Забираем список товаров с РАЗНЫМИ подкатегориями из базы данных с учетом выбранной категории и проходим по ним
    courses = await db.get_list_courses(subject[0])
    for course in courses:
        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           subject=subject, course=course[0])
        markup.insert(
            InlineKeyboardButton(text=course[1], callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)),
        InlineKeyboardButton(
            text='Домой',
            callback_data=make_callback_data(level=0)
        )
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def course_keyboard(subject, course):
    CURRENT_LEVEL = 2

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
    markup = InlineKeyboardMarkup()

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             subject=subject)),
        InlineKeyboardButton(
            text='Домой',
            callback_data=make_callback_data(level=0)
        )
    )
    return markup
