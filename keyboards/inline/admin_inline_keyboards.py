from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import admin_cd


async def admin_keyboard():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Показать все курсы',
                                 callback_data=admin_cd.new(action='show', aim='course'))
        ],
        [
            InlineKeyboardButton(text='Добавить курс',
                                 callback_data=admin_cd.new(action="add", aim='course')),
            InlineKeyboardButton(text='Изменить курс',
                                 callback_data=admin_cd.new(action="change", aim='course'))
        ],
        [
            InlineKeyboardButton(text='Удалить курс',
                                 callback_data=admin_cd.new(action="delete", aim='course'))
        ],
        [
            InlineKeyboardButton(text='Показать все предметы',
                                 callback_data=admin_cd.new(action='show', aim='subject'))
        ],
        [
            InlineKeyboardButton(text='Добавить предмет',
                                 callback_data=admin_cd.new(action="add", aim='subject')),
            InlineKeyboardButton(text='Изменить предмет',
                                 callback_data=admin_cd.new(action="change", aim='subject'))
        ],
        [
            InlineKeyboardButton(text='Удалить предмет',
                                 callback_data=admin_cd.new(action="delete", aim='subject'))
        ]
    ])
    return markup



