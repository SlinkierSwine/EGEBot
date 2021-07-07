from aiogram.dispatcher.filters.state import StatesGroup, State


# Course states

class AddCourseStates(StatesGroup):
    ask_name = State()
    ask_description = State()
    ask_price = State()
    ask_subject_id = State()


class ChangeCourseStates(StatesGroup):
    ask_id = State()
    ask_name = State()
    ask_description = State()
    ask_price = State()
    ask_subject_id = State()


class DeleteCourseStates(StatesGroup):
    ask_id = State()


# Subject states

class AddSubjectStates(StatesGroup):
    ask_name = State()


class ChangeSubjectStates(StatesGroup):
    ask_id = State()
    ask_name = State()
    ask_description = State()
    ask_price = State()
    ask_subject_id = State()


class DeleteSubjectStates(StatesGroup):
    ask_id = State()
    ask_confirm = State()
