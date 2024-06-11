from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.keyboards import group_kb
def register_group_handlers(dp:Dispatcher):
    dp.register_callback_query_handler(ready_to_order_call, lambda call: call.message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP])
    dp.register_message_handler(ready_to_order, lambda message: message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP])

async def ready_to_order(message: types.Message, state: FSMContext):
    await message.answer("Салам", reply_markup= group_kb())

async def ready_to_order_call(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.bot.send_message(chat_id= user_id, text="Привет бро")
    
    
