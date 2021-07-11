import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, db
from states.admin_states import DeleteCourseStates


@dp.message_handler(state=DeleteCourseStates.ask_id)
async def delete_course_id(message: Message, state: FSMContext):
    course_id = message.text

    if course_id == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        try:
            await db.delete_course({'id': course_id})

        except Exception as e:
            logging.error(e)
            await message.answer('Ошибка: ' + e.__str__())

        else:
            await message.answer('Курс успешно удален')

        await state.finish()
