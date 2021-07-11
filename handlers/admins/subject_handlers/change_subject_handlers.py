import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, db
from states.admin_states import ChangeSubjectStates


@dp.message_handler(state=ChangeSubjectStates.ask_id)
async def change_subject_id(message: Message, state: FSMContext):
    subject_id = message.text

    if subject_id == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        await state.update_data(id=subject_id)
        await message.answer('Введите название предмета\nЕсли не хотите его менять, напишете "-"')
        await ChangeSubjectStates.next()


@dp.message_handler(state=ChangeSubjectStates.ask_name)
async def change_subject_name(message: Message, state: FSMContext):
    name = message.text

    if name == 'Отмена':
        await state.finish()
        await message.answer('Действие отменено')

    else:
        if name != '-':
            await state.update_data(name=name)

        data = await state.get_data()

        try:
            await db.change_subject(data)
        except Exception as e:
            logging.error(e)
            await message.answer('Ошибка: ' + e.__str__())
        else:
            await message.answer('Предмет успешно изменен')

        await state.finish()
