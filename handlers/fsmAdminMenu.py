from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS
from keyboard.client_cb import cancel_markup
from database import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class FSMAdmin(StatesGroup):
    pizza_photo = State()
    pizza_name = State()
    pizza_info = State()
    pizza_price = State()


async def fsm_start(message: types.Message):
    if not message.from_user.id in ADMINS:
        await message.answer('ты лохэ')
    else:
        if message.chat.type == "private":
            await FSMAdmin.pizza_photo.set()
            await message.answer(f"Хало {message.from_user.first_name} "
                                 f"покажи пиццу.", reply_markup=cancel_markup)
        else:
            await message.answer("в группе пиццу не добавишь((")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pizza_photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('как зовут этого колобка', reply_markup=cancel_markup)


async def load_pizza_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pizza_name'] = message.text
        await message.reply(f"что такое {data['pizza_name']}?", reply_markup=cancel_markup)
    await FSMAdmin.next()


async def load_pizza_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pizza_info'] = message.text
    await FSMAdmin.next()
    await message.reply(f"За скоко ты это впихиваешь?", reply_markup=cancel_markup)


async def load_pizza_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['pizza_price'] = int(message.text)
        except:
            await message.answer('Але цену введи а не твои фантазии')
        await bot.send_photo(message.from_user.id, data['pizza_photo'],
                             caption=f"{data['pizza_name']},\n{data['pizza_info']},\n{data['pizza_price']}")

    await bot_db.sql_command_insert(state)
    await state.finish()

async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Ну и пошел ты')


async def delete_data(message: types.Message):
    if not message.from_user.id in ADMINS:
        await message.reply('Ты не мой босс!')
    else:
        dishes = await bot_db.sql_command_all()
        for dish in dishes:
            await bot.send_photo(message.from_user.id, dish[0],
                                 caption=f"{dish[1]}, {dish[2]} стоит: {dish[3]}",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"delete {dish[1]}",
                                         callback_data=f"delete {dish[1]}"
                                     )
                                 ))


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Удален из БД", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

def register_handlers_fsm_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands=['cancel'], commands_prefix='\!.')
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['create'])
    dp.register_message_handler(load_photo, state=FSMAdmin.pizza_photo,
                                content_types=['photo'])
    dp.register_message_handler(load_pizza_name, state=FSMAdmin.pizza_name)
    dp.register_message_handler(load_pizza_info, state=FSMAdmin.pizza_info)
    dp.register_message_handler(load_pizza_price, state=FSMAdmin.pizza_price)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))
