from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from config import dp, bot
from database.bot_db import sql_command_random
from random import choice

async def mem(message: types.Message):
    list = ['media/a2.jpg', 'media/a1.jpg', 'media/a3.jpg']
    photo = open(choice(list), 'rb')
    await bot.send_photo(message.chat.id, photo=photo)

async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('NEXT', callback_data='button_1')
    markup.add(button_1)
    question = "Who created GeekTech?"
    answers = ['Esen', 'Marlen', 'Aidar Bakirov', 'Aitegin']
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        correct_option_id=3,
        type='quiz',
        open_period=10,
        is_anonymous=True,
        explanation='Он школьник',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )

async def pin(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Это не ответ на сообщение!')
    else:
        await bot.pin_chat_message(message.chat.id, message.message_id)

async def show_random(message: types.Message):
    await sql_command_random(message)

def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(show_random, commands=['get'])