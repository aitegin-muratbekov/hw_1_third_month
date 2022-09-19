from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS


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
                                 f"покажи пиццу.",)
        else:
            await message.answer("в группе пиццу не добавишь((")



id = 0
async def load_photo(message: types.Message, state: FSMContext):
    global id
    async with state.proxy() as data:
        data['id'] = id
        id += 1
        data['pizza_photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('как зовут этого колобка')
async def load_pizza_name(message: types.Message, state: FSMContext):
    async with state.proxy as data:
        data['pizza_name'] = message.text
    await FSMAdmin.next()
    await message.reply(f"что такое {data['name']}?")

async def load_pizza_info(message: types.Message, state: FSMContext):
    async with state.proxy as data:
        data['pizza_info'] = message.text
    await FSMAdmin.next()
    await message.reply(f"За скоко ты это впихиваешь?")

async def load_pizza_price(message: types.Message, state: FSMContext):
    async with state.proxy as data:
        try:
            data['pizza_price'] = int(message.text)
        except:
            message.answer('Але цену введи а не твои фантазии')
        await bot.send_photo(message.from_user.id, data['pizza_photo'],
                             caption=f"{data['pizza_name']},\n {data['pizza info']},\n {data['pizza_price']}")

    await state.finish()


def register_handlers_fsm_admin(dp: Dispatcher):

    dp.register_message_handler(fsm_start, commands=['create'])
    dp.register_message_handler(load_photo, state=FSMAdmin.pizza_photo,
                                content_types=['photo'])
    dp.register_message_handler(load_pizza_name, state=FSMAdmin.pizza_name)
    dp.register_message_handler(load_pizza_info, state=FSMAdmin.pizza_info)
    dp.register_message_handler(load_pizza_price, state=FSMAdmin.pizza_price)
