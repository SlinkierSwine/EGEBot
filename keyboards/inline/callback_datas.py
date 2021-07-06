from aiogram.utils.callback_data import CallbackData


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, subject="0", course="0"):
    return menu_cd.new(level=level, subject=subject, course=course)


menu_cd = CallbackData("show_menu", "level", "subject", "course")
