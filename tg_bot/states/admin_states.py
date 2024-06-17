from aiogram.dispatcher.filters.state import StatesGroup, State

class admin(StatesGroup):
    add_fio = State()
    add_number = State()
    add_adress = State()
    select_category = State()
    select = State()
    add_comment = State()
    decline = State()
    order = State()

class reclamation(StatesGroup):
    add_fio = State()
    add_number = State()
    add_adress = State()
    select_category = State()
    select = State()
    add_comment = State()
    
class user(StatesGroup):
    add_photo = State()

    
