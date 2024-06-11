from aiogram.dispatcher.filters.state import StatesGroup, State

class admin(StatesGroup):
    add_fio = State()
    add_number = State()
    add_adress = State()
    select_category = State()
    add_comment = State()

    