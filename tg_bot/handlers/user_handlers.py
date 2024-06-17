from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from tg_bot.DBSM import get_order_data, yes_zamer, get_recl_data
from tg_bot.keyboards import photo_add_kb, decline_photo_kb, done
from tg_bot.states import user
import os, string, random

admin_ids = [1446691883, 1842494556] 

def register_group_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(ready_to_order_call, lambda call: call.message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP], text_startswith = "i_can")
    dp.register_callback_query_handler(add_photo_process, text="add_photo")
    dp.register_callback_query_handler(done_rec, text="done")
    dp.register_message_handler(add_photo, state = user.add_photo, content_types = ["photo"])
    dp.register_callback_query_handler(cancel_add, state = user.add_photo, text="decline")


async def ready_to_order_call(call: types.CallbackQuery, state: FSMContext): #когда пользоваптель в группе нажал я смогу
    user_id = call.from_user.id 
    id = call.message.text.split("\n")[-1].split(" - ")[1]
    await call.message.delete()
    if call.data == "i_can":
        for i in admin_ids:
            await call.message.bot.send_message(chat_id= i, text= f"Работник @{call.from_user.username} откликнулся на заявку с номером {id}") 
        data = get_order_data(id, call.from_user.id, call.from_user.username)
        await call.message.bot.send_message(chat_id= user_id, text= f"❗У Вас новая заявка на замер❗\nКатегория - <i>{data[3]}</i>\nНомер телефона заказчика - <i>{data[0]}</i>\nАдрес заказчика - <i>{data[1]}</i>\nИмя заказчика - <i>{data[4]}</i>\nКомментарий к заявке - <i>{data[2]}</i>\nНомер заявки - <i>{id}</i>\n\nФотография замера - <i>не добавлена</i> ❌", reply_markup= photo_add_kb())
    else:
        for i in admin_ids:
            await call.message.bot.send_message(chat_id= i, text= f"Работник @{call.from_user.username} откликнулся на рекламацию с номером {id}") 
        data = get_recl_data(id, call.from_user.id)
        await call.message.bot.send_message(chat_id= user_id, text= f"❗У Вас новая рекламация❗\nКатегория - <i>{data[3]}</i>\nНомер телефона заказчика - <i>{data[0]}</i>\nАдрес заказчика - <i>{data[1]}</i>\nИмя заказчика - <i>{data[4]}</i>\nКомментарий - <i>{data[2]}</i>\nНомер - <i>{id}</i>", reply_markup= done())



async def add_photo_process(call: types.CallbackQuery, state: FSMContext): #пользователь нажал на кнопку добавить фото замеров
    async with state.proxy() as data:
        data["message"] = await call.message.answer("Отправьте фото замера", reply_markup= decline_photo_kb())
        data["main"] = call.message
    await user.add_photo.set()


async def add_photo(message: types.Message, state: FSMContext): #добавление фотографии
    photo = message.photo[-1]
    async with state.proxy() as data:
        mess = data["message"]
        await mess.delete()
        main = data["main"]

    arr = main.text.split("\n\n")
    new_text = arr[0] + "\n\nФотография замера - <i>добавлена</i> ✅"
    await main.edit_text(text = new_text, reply_markup = None)
    id = arr[0].split("\n")[6].split(" - ")[1]
    yes_zamer(id)

    def generate_random_string(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    if not os.path.isdir("tg_bot/images"):
        os.mkdir("tg_bot/images")

    name = generate_random_string(20)
    while os.path.isdir(f"tg_bot/images/{name}.jpg"):
        name = generate_random_string(20)
    
    await photo.download(destination= f"tg_bot/images/{name}.jpg")
    for i in admin_ids:
        await message.bot.send_photo(chat_id = i, photo = InputFile(f"tg_bot/images/{name}.jpg"), caption= f"Работник добавил замер к заявке номер {id}")
    await state.finish()
    
    
    
async def cancel_add(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

async def done_rec(call: types.CallbackQuery, state: FSMContext):
    text = call.message.text
    await call.message.edit_text(text=f"{text}\n\nВыполнена✅",reply_markup=None)
    id = call.message.text.split("\n")[-1].split(" - ")[1]
    for i in admin_ids:
        await call.message.bot.send_message(chat_id= i, text=f"Работник {call.from_user.username} выполнил рекламацию номер {id}")

