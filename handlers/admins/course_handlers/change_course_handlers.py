import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode

from loader import dp, db
from states.admin_states import ChangeCourseStates


@dp.message_handler(state=ChangeCourseStates.ask_id)
async def change_course_id(message: Message, state: FSMContext):
    course_id = message.text
    await state.update_data(id=course_id)
    await message.answer('Введите название курса\nЕсли не хотите его менять, напишете "-"')
    await ChangeCourseStates.next()


@dp.message_handler(state=ChangeCourseStates.ask_name)
async def change_course_name(message: Message, state: FSMContext):
    name = message.text

    if name != '-':
        await state.update_data(name=name)

    await message.answer('Введите описание курса\nЕсли не хотите его менять, напишете "-"')

    await ChangeCourseStates.next()


@dp.message_handler(state=ChangeCourseStates.ask_description)
async def change_course_description(message: Message, state: FSMContext):
    description = message.text

    if description != '-':
        await state.update_data(description=description)

    await message.answer('Введите цену курса\nЕсли не хотите её менять, напишете "-"')

    await ChangeCourseStates.next()


@dp.message_handler(state=ChangeCourseStates.ask_price)
async def change_course_price(message: Message, state: FSMContext):
    price = message.text

    if price != '-':
        await state.update_data(price=price)

    subjects = await db.get_list_subjects()
    text = ''
    for s in subjects:
        text += f'Название: <b>{s[1]}</b>, id: <b>{s[0]}</b>\n'

    await message.answer(
        f'Введите id предмета курса\nЕсли не хотите его менять, напишете "-".\n\nДоступные предметы:\n\n{text}',
        parse_mode=ParseMode.HTML
    )

    await ChangeCourseStates.next()


@dp.message_handler(state=ChangeCourseStates.ask_subject_id)
async def change_course_subject_id(message: Message, state: FSMContext):
    subject_id = message.text

    if subject_id != '-':
        await state.update_data(subject_id=subject_id)

    data = await state.get_data()

    try:
        await db.change_course(data)
    except Exception as e:
        logging.error(e)
        await message.answer('Ошибка: ' + e.__str__())
    else:
        await message.answer('Курс успешно изменен')

    await state.finish()
