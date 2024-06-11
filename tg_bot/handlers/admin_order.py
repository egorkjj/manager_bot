from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.states import admin
from tg_bot.keyboards import category, decline
from tg_bot.DBSM import add_order_metadata
import time

def register_admin_order_handlers(dp: Dispatcher):
    dp.register_message_handler(add_order, commands=["add"])
    dp.register_message_handler(add_fio, state = admin.add_fio)
    dp.register_message_handler(add_adress, state = admin.add_adress)
    dp.register_message_handler(add_number, state = admin.add_number)
    dp.register_message_handler(add_comment, state = admin.add_comment)
    dp.register_callback_query_handler(select_category, state = admin.select_category, text_startswith = "cat")
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

    await admin.add_comment.set()
    await call.message.answer("Категория добавлена. Теперь напишите комментарий к заказу для заказчика. Если Вы не хотите ничего комментировать, просто напишите 'нет комментария'", reply_markup= decline())


async def add_comment(message: types.Message, state: FSMContext): # последний шаг - админ добавил коммент
    async with state.proxy() as data:
        data["comment"] = message.text

    wait = await message.answer("Комментарий добавлен. Формирую заявку на замер...")
    async with state.proxy() as data:
        id = add_order_metadata(message.from_user.username, data["number"], data["adress"], data["comment"], data["category"])

    time.sleep(1)
    await wait.delete()
    await message.answer(f"Заявка на замер добавлена.\n❗❗❗<b><i> Уникальной идентификатор заявки - {id} </i></b>❗❗❗\nСообщение с заявкой переслано в группу с работниками, когда на нее кто-то откликнется, Вы будете уведомлены.\n\nКогда работник сделает замеры и отправит их боту, они будут сразу же отправлены Вам. Когда после совершения замеров клиент оформит заказ, напишите мне команду <b><i>/order</i></b>, чтобы подтвердить оформление заказа, и тогда работник, который совершал замеры, сразу же будет уведомен от бота о том, что заказ создан.\n\nОзнакомиться с актуальной информацией по заявкам на замеры и заказам можно отправив мне команду <b><i>/excel</i></b> - и я пришлю Вам информацию в формате таблицы.")
    await state.finish()


async def decline_all(call: types.CallbackQuery, state: FSMContext): # отмена добавления)
    if await state.get_state() in ["admin:add_fio", "admin:add_comment", "admin:add_adress", "admin:add_number"]:
        await state.finish()
        await call.message.answer("Хорошо, добавление заявки на замер отмененено. Если решите добавить заявку, отправьте боту комнаду /add.")

