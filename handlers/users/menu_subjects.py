from typing import Union

from aiogram.types import Message, CallbackQuery

from keyboards.default.menu import menu_kb
from keyboards.inline.callback_datas import menu_cd
from keyboards.inline.menu_subjects import list_subjects_keyboard, list_courses_keyboard, course_keyboard
from loader import dp, db


@dp.message_handler(commands=['start'])
async def bot_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu_kb)


@dp.message_handler(lambda message: message.text == 'Предметы')
async def list_subjects(message: Union[CallbackQuery, Message], **kwargs):
    markup = await list_subjects_keyboard()

    if isinstance(message, Message):
        await message.answer("Доступные предметы:", reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text('Доступные предметы:', reply_markup=markup)


async def list_courses(callback: CallbackQuery, subject, **kwargs):
    markup = await list_courses_keyboard(subject)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text('Доступные курсы:', reply_markup=markup)


# Функция, которая отдает уже кнопку Купить товар по выбранному товару
async def show_course(callback: CallbackQuery, subject, course, **kwargs):
    markup = await course_keyboard(subject, course)

    item = await db.get_course(course)
    text = f'Купить {item[1]} за {item[3]}'

    await callback.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    subject = callback_data.get("subject")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    course = callback_data.get("course")

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_subjects,  # Отдаем категории
        "1": list_courses,  # Отдаем подкатегории
        "2": show_course  # Отдаем товары
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        subject=subject,
        course=course
    )
