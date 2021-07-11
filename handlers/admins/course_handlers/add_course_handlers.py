from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode

from loader import dp, db
from states.admin_states import AddCourseStates


@dp.message_handler(state=AddCourseStates.ask_name)
async def add_course_name(message: Message, state: FSMContext):
    course_name = message.text

    if course_name == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        await state.update_data(course_name=course_name)

        await message.answer('Введите описание курса')
        await AddCourseStates.next()


@dp.message_handler(state=AddCourseStates.ask_description)
async def add_course_description(message: Message, state: FSMContext):
    course_description = message.text

    if course_description == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        await state.update_data(course_description=course_description)

        await message.answer('Введите цену курса')
        await AddCourseStates.next()


@dp.message_handler(state=AddCourseStates.ask_price)
async def add_course_price(message: Message, state: FSMContext):
    course_price = message.text

    if course_price == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        await state.update_data(course_price=course_price)

        subjects = await db.get_list_subjects()
        text = ''
        for s in subjects:
            text += f'Название: <b>{s[1]}</b>, id: <b>{s[0]}</b>\n'

        await message.answer(f'Введите id предмета курса. Доступные предметы:\n\n{text}',
                             parse_mode=ParseMode.HTML)
        await AddCourseStates.next()


@dp.message_handler(state=AddCourseStates.ask_subject_id)
async def add_course_subject_id(message: Message, state: FSMContext):
    course_subject_id = message.text

    if course_subject_id == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        data = await state.get_data()
        name = data.get('course_name')
        description = data.get('course_description')
        price = data.get('course_price')

        try:
            await db.add_course(name, description, price, course_subject_id)
        except Exception as e:
            await message.answer(e.__str__())
        else:
            await message.answer('Курс успешно добавлен')
        await state.finish()
