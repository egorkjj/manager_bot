from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def group_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Я смогу сделать", callback_data="i_can"))
    return kb

def category():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Окна", callback_data="cat_0"))
    kb.add(InlineKeyboardButton(text="Металлические двери", callback_data="cat_1"))
    kb.add(InlineKeyboardButton(text="Двери ПВХ", callback_data="cat_2"))
    kb.add(InlineKeyboardButton(text="Межкомнатные двери", callback_data="cat_3"))
    kb.add(InlineKeyboardButton(text="Отменить добавление заявки", callback_data="decline"))
    return kb

def decline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отменить добавление заявки" , callback_data="decline"))
    return kb
