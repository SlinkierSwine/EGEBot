from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, db
from states.admin_states import AddSubjectStates


@dp.message_handler(state=AddSubjectStates.ask_name)
async def add_subject_name(message: Message, state: FSMContext):
    subject_name = message.text

    try:
        await db.add_subject(subject_name)
    except Exception as e:
        await message.answer(e.__str__())
    else:
        await message.answer('Предмет добавлен')

    await state.finish()
