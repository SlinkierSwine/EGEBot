from aiogram.types import Message, CallbackQuery

from config import ADMINS
from keyboards.inline.admin_inline_keyboards import admin_keyboard
from keyboards.inline.callback_datas import admin_cd
from loader import dp, db
from states.admin_states import AddCourseStates, AddSubjectStates, ChangeCourseStates, \
    ChangeSubjectStates, DeleteCourseStates, DeleteSubjectStates


def is_admin(func):
    async def wrapper(message: Message):
        if message.from_user.id in ADMINS:
            return await func(message)
    return wrapper


@is_admin
@dp.message_handler(commands='admin')
async def admin(message: Message):
    markup = await admin_keyboard()
    await message.answer('Выберите действие.\nЧтобы отменить любое действие напишите "Отмена":', reply_markup=markup)


@dp.callback_query_handler(admin_cd.filter(action='add'))
async def add(call: CallbackQuery, callback_data: dict):
    aim = callback_data.get('aim')

    if aim == 'course':
        await call.message.edit_text('Введите название курса:', reply_markup=None)
        await AddCourseStates.ask_name.set()

    elif aim == 'subject':
        await call.message.edit_text('Введите название предмета:', reply_markup=None)
        await AddSubjectStates.ask_name.set()


@dp.callback_query_handler(admin_cd.filter(action='change'))
async def change(call: CallbackQuery, callback_data: dict):
    aim = callback_data.get('aim')

    if aim == 'course':
        await call.message.edit_text('Введите id курса:', reply_markup=None)
        await ChangeCourseStates.ask_id.set()

    elif aim == 'subject':
        await call.message.edit_text('Введите id предмета:', reply_markup=None)
        await ChangeSubjectStates.ask_id.set()


@dp.callback_query_handler(admin_cd.filter(action='delete'))
async def delete(call: CallbackQuery, callback_data: dict):
    aim = callback_data.get('aim')

    if aim == 'course':
        await call.message.edit_text('Введите id курса:', reply_markup=None)
        await DeleteCourseStates.ask_id.set()

    elif aim == 'subject':
        await call.message.edit_text('Введите id предмета:', reply_markup=None)
        await DeleteSubjectStates.ask_id.set()


@dp.callback_query_handler(admin_cd.filter(action='show'))
async def delete(call: CallbackQuery, callback_data: dict):
    aim = callback_data.get('aim')
    text = await get_list_text(aim)

    if aim == 'course':
        await call.message.edit_text('Список всех курсов\n\n' + text, reply_markup=None)

    if aim == 'subject':
        await call.message.edit_text('Список всех предметов\n\n' + text, reply_markup=None)


async def get_list_text(aim):
    text = ''

    if aim == 'course':
        courses = await db.get_all_courses()

        for c in courses:
            text += f'Название: <b>{c[1]}</b>\nid: <b>{c[0]}</b>\nПредмет: <b>{c[3]}</b>\nid предмета: <b>{c[2]}</b>\n\n'

    elif aim == 'subject':
        subjects = await db.get_all_subjects()

        for s in subjects:
            text += f'Название: <b>{s[1]}</b>\nid: <b>{s[0]}</b>\n\n'

    return text
