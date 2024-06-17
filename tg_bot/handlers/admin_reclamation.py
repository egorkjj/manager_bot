from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.DBSM import add_recl_metadata
from tg_bot.states import reclamation 
from tg_bot.keyboards import category_rec, decline_reclamation_add, group_kb_rec, decline_ny_rec
import time
categories = {
    "0": "Окна и двери ПВХ",
    "1": "Металлические двери",
    "2": "Межкомнатные двери",
    "3": "Ворота",
    "4": "Рольшторы, жалюзи"
}

admin_ids = [1446691883, 1842494556] 

def registrer_reclamation(dp: Dispatcher):
    dp.register_message_handler(add_order, lambda message: message.from_user.id in admin_ids, commands=["reclamation"])
    dp.register_message_handler(add_fio, state = reclamation.add_fio)
    dp.register_message_handler(add_adress, state = reclamation.add_adress)
    dp.register_message_handler(add_number, state = reclamation.add_number)
    dp.register_callback_query_handler(select_yes_no, state = reclamation.select, text_startswith = "rec_comment")
    dp.register_message_handler(add_comment, state = reclamation.add_comment)
    dp.register_callback_query_handler(select_category, state = reclamation.select_category, text_startswith = "rec_cat")
    dp.register_callback_query_handler(decline_all, text="decline_rec", state = "*")


async def add_order(message: types.Message, state: FSMContext): #шаг 1 - админ ввел команду /add
    await reclamation.add_fio.set()
    await message.answer("Введите, пожалуйста, ФИО заказчика", reply_markup= decline_reclamation_add())

async def add_fio(message: types.Message, state: FSMContext): #шаг 2 - админ ввел фио
    async with state.proxy() as data:
        data["fio"] = message.text

    await reclamation.add_adress.set()
    await message.answer("ФИО принято. Теперь введите адрес заказчика.", reply_markup= decline_reclamation_add())


async def add_adress(message: types.Message, state: FSMContext): #шаг 3 - админ ввел адрес 
    async with state.proxy() as data:
        data["adress"] = message.text

    await reclamation.add_number.set()
    await message.answer("Адрес добавлен. Введите номер телефона заказчика.", reply_markup= decline_reclamation_add())

async def add_number(message: types.Message, state: FSMContext): # шаг 4 - админ ввел номер телефона
    async with state.proxy() as data:
        data["number"] = message.text

    await reclamation.select_category.set()
    await message.answer("Номер телефона добавлен. Выберите категорию.", reply_markup=category_rec())


async def select_category(call: types.CallbackQuery, state: FSMContext): # шаг 5 - админ выбрал категорию
    cat = int(call.data.split("_")[2])
    async with state.proxy() as data:
        data["category"] = cat

    await reclamation.select.set()
    await call.message.answer("Категория добавлена. Есть ли у Вас комментарий для работника?", reply_markup= decline_ny_rec())


async def select_yes_no(call: types.CallbackQuery, state: FSMContext):
    if call.data.split("_")[2] == "no":
        async with state.proxy() as data:
            data["comment"] = "отсутствует"
    
        wait = await call.message.answer("Хорошо, формирую рекламацию...")
        async with state.proxy() as data:
            id = add_recl_metadata(data["number"], data["adress"], data["comment"], data["category"], data["fio"])
            cat = int(data["category"])
            if cat != 2:
                await call.message.bot.send_message(chat_id = -1002212506866, text= f"❗❗❗Появилась новая рекламация❗❗❗\nКатегория - <i>{categories[f'{cat}']}</i>\nАдрес клиента - <i>{data['adress']}</i>\nНомер телефона клиента - <i>{data['number']}</i>\nКомментарий: <i>{data['comment']}</i>\nНомер рекламации - {id}", reply_markup=group_kb_rec())

        time.sleep(1)
        await wait.delete()
        await call.message.answer(f"Рекламация добавлена.\n❗<b><i>Номер - {id}</i></b>❗")
        await state.finish()
    else:
        await call.message.edit_text("Хорошо, введите комментарий ниже", reply_markup= None)
        await reclamation.add_comment.set()


async def add_comment(message: types.Message, state: FSMContext): # последний шаг - админ добавил коммент
    async with state.proxy() as data:
        data["comment"] = message.text
    
    wait = await message.answer("Комментарий добавлен. Формирую рекламацию...")
    async with state.proxy() as data:
        id = add_recl_metadata(data["number"], data["adress"], data["comment"], data["category"], data["fio"])
        cat = int(data["category"])
        if cat != 2:
            await message.bot.send_message(chat_id = -1002212506866, text= f"❗❗❗Появилась новая рекламация❗❗❗\nКатегория - <i>{categories[f'{cat}']}</i>\nАдрес клиента - <i>{data['adress']}</i>\nНомер телефона клиента - <i>{data['number']}</i>\nКомментарий к заявке: <i>{data['comment']}</i>\nНомер - {id}", reply_markup=group_kb_rec())

    time.sleep(1)
    await wait.delete()
    await message.answer(f"Рекаламация добавлена.\n❗<b><i>Номер - {id}</i></b>❗")
    await state.finish()


async def decline_all(call: types.CallbackQuery, state: FSMContext): # отмена добавления
    if await state.get_state() in ["reclamation:add_fio", "reclamation:add_comment", "reclamation:add_adress", "reclamation:add_number", "reclamation:select_category", "reclamation:select"]:
        await state.finish()
        await call.message.answer("Хорошо, добавление рекламации отмененено. Если решите добавить рекламацию, отправьте боту комнаду /reclamation.")