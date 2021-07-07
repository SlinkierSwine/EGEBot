import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, db
from states.admin_states import DeleteSubjectStates


@dp.message_handler(state=DeleteSubjectStates.ask_id)
async def delete_subject_id(message: Message, state: FSMContext):
    subject_id = message.text
    await state.update_data(id=subject_id)

    courses = await db.get_list_courses(subject_id)

    if courses:

        text = ''
        for c in courses:
            text += f'Название: <b>{c[1]}</b>, id: <b>{c[0]}</b>\n'

        await message.answer('У данного предмета есть следующие курсы.'
                             ' При удалении предмета эти курсы так же удалятся.\n\n' +
                             text +
                             '\nПродолжить?("+"/"-")')
        await DeleteSubjectStates.next()

    else:
        try:
            await db.delete_subject(await state.get_data())

        except Exception as e:
            logging.error(e)
            await message.answer('Ошибка: ' + e.__str__())

        else:
            await message.answer('Предмет успешно удален')

        await state.finish()


@dp.message_handler(state=DeleteSubjectStates.ask_confirm)
async def delete_subject_confirm(message: Message, state: FSMContext):
    confirmed = message.text

    if confirmed == '+':
        try:
            await db.delete_subject(await state.get_data())

        except Exception as e:
            logging.error(e)
            await message.answer('Ошибка: ' + e.__str__())

        else:
            await message.answer('Предмет успешно удален')

    await state.finish()
