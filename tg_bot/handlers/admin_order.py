from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.states import admin
from tg_bot.keyboards import category, decline, group_kb, levcmo, order_decline, decline_ny
from tg_bot.DBSM import add_order_metadata, decline_order, yes_order
import time

categories = {
    "0": "Окна и двери ПВХ",
    "1": "Металлические двери",
    "2": "Межкомнатные двери",
    "3": "Ворота",
    "4": "Рольшторы, жалюзи"
}

admin_ids = [1446691883, 1842494556] 


def register_admin_order_handlers(dp: Dispatcher):
    dp.register_message_handler(add_order, lambda message: message.from_user.id in admin_ids, commands=["add"])
    dp.register_message_handler(decline_order_step1, lambda message: message.from_user.id in admin_ids, commands=["decline"])
    dp.register_message_handler(add_order_step1, lambda message: message.from_user.id in admin_ids, commands=["order"])
    dp.register_message_handler(add_order_step2, state = admin.order)
    dp.register_message_handler(decline_order_step2, state = admin.decline)
    dp.register_message_handler(add_fio, state = admin.add_fio)
    dp.register_message_handler(add_adress, state = admin.add_adress)
    dp.register_message_handler(add_number, state = admin.add_number)
    dp.register_callback_query_handler(select_yes_no, state = admin.select, text_startswith = "comment")
    dp.register_message_handler(add_comment, state = admin.add_comment)
    dp.register_callback_query_handler(select_category, state = admin.select_category, text_startswith = "cat")
    dp.register_callback_query_handler(decline_decline, state = admin.decline, text="rm")
    dp.register_callback_query_handler(add_order_no, state = admin.order, text="rmr")
    dp.register_callback_query_handler(decline_all, text="decline", state = "*")


async def add_order(message: types.Message, state: FSMContext): #шаг 1 - админ ввел команду /add
    await admin.add_fio.set()
    await message.answer("Введите, пожалуйста, ФИО заказчика", reply_markup= decline())


async def add_fio(message: types.Message, state: FSMContext): #шаг 2 - админ ввел фио
    async with state.proxy() as data:
        data["fio"] = message.text

    await admin.add_adress.set()
    await message.answer("ФИО принято. Теперь введите адрес заказчика.", reply_markup= decline())


async def add_adress(message: types.Message, state: FSMContext): #шаг 3 - админ ввел адрес 
    async with state.proxy() as data:
        data["adress"] = message.text

    await admin.add_number.set()
    await message.answer("Адрес добавлен. Введите номер телефона заказчика.", reply_markup= decline())

async def add_number(message: types.Message, state: FSMContext): # шаг 4 - админ ввел номер телефона
    async with state.proxy() as data:
        data["number"] = message.text

    await admin.select_category.set()
    await message.answer("Номер телефона добавлен. Выберите категорию предмета для замера.", reply_markup=category())


async def select_category(call: types.CallbackQuery, state: FSMContext): # шаг 5 - админ выбрал категорию
    cat = int(call.data.split("_")[1])
    async with state.proxy() as data:
        data["category"] = cat

    await admin.select.set()
    await call.message.answer("Категория добавлена. Есть ли у Вас комментарий к заявке для работника?", reply_markup= decline_ny())


async def select_yes_no(call: types.CallbackQuery, state: FSMContext):
    if call.data.split("_")[1] == "no":
        async with state.proxy() as data:
            data["comment"] = "отсутствует"
    
        wait = await call.message.answer("Хорошо, формирую заявку на замер...")
        async with state.proxy() as data:
            id = add_order_metadata(data["number"], data["adress"], data["comment"], data["category"], data["fio"])
            cat = int(data["category"])
            if cat != 2:
                await call.message.bot.send_message(chat_id = -1002212506866, text= f"❗❗❗Появилась новая заявка на замер❗❗❗\nКатегория замера - <i>{categories[f'{cat}']}</i>\nАдрес клиента - <i>{data['adress']}</i>\nНомер телефона клиента - <i>{data['number']}</i>\nКомментарий к заявке: <i>{data['comment']}</i>\nНомер заявки - {id}", reply_markup=group_kb())

        time.sleep(1)
        await wait.delete()
        await call.message.answer(f"Заявка на замер добавлена.\n❗<b><i>Номер заявки - {id}</i></b>❗")
        await state.finish()
    else:
        await call.message.edit_text("Хорошо, введите комментарий ниже", reply_markup= None)
        await admin.add_comment.set()


async def add_comment(message: types.Message, state: FSMContext): # последний шаг - админ добавил коммент
    async with state.proxy() as data:
        data["comment"] = message.text
    
    wait = await message.answer("Комментарий добавлен. Формирую заявку на замер...")
    async with state.proxy() as data:
        id = add_order_metadata(data["number"], data["adress"], data["comment"], data["category"], data["fio"])
        cat = int(data["category"])
        if cat != 2:
            await message.bot.send_message(chat_id = -1002212506866, text= f"❗❗❗Появилась новая заявка на замер❗❗❗\nКатегория замера - <i>{categories[f'{cat}']}</i>\nАдрес клиента - <i>{data['adress']}</i>\nНомер телефона клиента - <i>{data['number']}</i>\nКомментарий к заявке: <i>{data['comment']}</i>\nНомер заявки - {id}", reply_markup=group_kb())

    time.sleep(1)
    await wait.delete()
    await message.answer(f"Заявка на замер добавлена.\n❗<b><i>Номер заявки - {id}</i></b>❗")
    await state.finish()


async def decline_all(call: types.CallbackQuery, state: FSMContext): # отмена добавления
    if await state.get_state() in ["admin:add_fio", "admin:add_comment", "admin:add_adress", "admin:add_number", "admin:select_category", "admin:select"]:
        await state.finish()
        await call.message.answer("Хорошо, добавление заявки на замер отмененено. Если решите добавить заявку, отправьте боту комнаду /add.")



async def decline_order_step1(message: types.Message, state: FSMContext):
    await message.answer("Введите номер заявки, которую хотите отменить", reply_markup= levcmo())
    await admin.decline.set()

async def decline_order_step2(message: types.Message, state: FSMContext):
    result = decline_order(message.text)
    if result == False:
        await message.answer("Упс, заявки с таким номером не найдено... Введите заново, или нажмите кнопку ниже", reply_markup= levcmo())
        return
    if result == None:
        await message.answer(f"Заявка {message.text} отменена")
        await state.finish()
    else:
        await message.answer(f"Заявка {message.text} отменена")
        await state.finish()
        await message.bot.send_message(chat_id= int(result), text = f"Заявка на замер с номером {message.text} отменена!")

async def decline_decline(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()



async def add_order_step1(message: types.Message, state: FSMContext):
    await message.answer("Введите номер заявки", reply_markup=order_decline())
    await admin.order.set()


async def add_order_step2(message: types.Message, state: FSMContext):
    result = yes_order(message.text)
    if result == False:
        await message.answer("Упс, заявки с таким номером не найдено... введите заново или нажмите кнопку ниже", reply_markup= order_decline())
        return
    await message.answer(f"Готово! Заказ на заявку с номером {message.text} подтвержден!")
    if result[0] != None:
        await message.bot.send_message(chat_id= int(result[0]), text=f"У Вас новый заказ! Номер заявки на замер - {result[-1]}\nАдрес заказчика - {result[1]}\nФИО заказчика - {result[2]}\nТелефон заказчика - {result[3]}\nКатегория - {result[4]}")
    await state.finish()


async def add_order_no(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
