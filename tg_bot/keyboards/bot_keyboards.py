from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def group_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Я смогу сделать ✅", callback_data="i_can"))
    return kb

def category():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Окна и двери ПВХ", callback_data="cat_0"))
    kb.add(InlineKeyboardButton(text="Металлические двери", callback_data="cat_1"))
    kb.add(InlineKeyboardButton(text="Межкомнатные двери", callback_data="cat_2"))
    kb.add(InlineKeyboardButton(text="Ворота", callback_data= "cat_3"))
    kb.add(InlineKeyboardButton(text="Рольшторы и жалюзи", callback_data= "cat_4"))
    kb.add(InlineKeyboardButton(text="Отменить добавление заявки ❌", callback_data="decline"))
    return kb

def decline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отменить добавление заявки ❌" , callback_data="decline"))
    return kb

def decline_reclamation_add():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отменить добавление рекламации ❌" , callback_data="decline_rec"))
    return kb

def photo_add_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Добавить фотографии замера", callback_data="add_photo"))
    return kb

def decline_photo_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отменить добавление ❌" , callback_data="decline"))
    return kb


def levcmo():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Вернуться ❌" , callback_data="rm"))
    return kb

def order_decline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отменить подтверждение заказа ❌" , callback_data="rmr"))
    return kb

def decline_ny():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="есть комментарий", callback_data="comment_yes"))
    kb.add(InlineKeyboardButton(text="нет комментария", callback_data="comment_no"))
    kb.add(InlineKeyboardButton(text="Отменить добавление заявки ❌" , callback_data="decline"))
    return kb

def group_kb_rec():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Я смогу сделать ✅", callback_data="i_can_rec"))
    return kb

def done():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Сделано ✅", callback_data="done"))
    return kb

def category_rec():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Окна и двери ПВХ", callback_data="rec_cat_0"))
    kb.add(InlineKeyboardButton(text="Металлические двери", callback_data="rec_cat_1"))
    kb.add(InlineKeyboardButton(text="Межкомнатные двери", callback_data="rec_cat_2"))
    kb.add(InlineKeyboardButton(text="Ворота", callback_data= "rec_cat_3"))
    kb.add(InlineKeyboardButton(text="Рольшторы и жалюзи", callback_data= "rec_cat_4"))
    kb.add(InlineKeyboardButton(text="Отменить добавление рекламации ❌", callback_data="decline_rec"))
    return kb

def decline_ny_rec():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="есть комментарий", callback_data="rec_comment_yes"))
    kb.add(InlineKeyboardButton(text="нет комментария", callback_data="rec_comment_no"))
    kb.add(InlineKeyboardButton(text="Отменить добавление рекламации ❌" , callback_data="decline_rec"))
    return kb