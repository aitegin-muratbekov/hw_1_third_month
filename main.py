import logging

from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from random import choice

from config import bot, dp


@dp.message_handler(commands=['mem'])
async def mem(message: types.Message):
    list = ['media/a2.jpg', 'media/a1.jpg', 'media/a3.jpg']
    photo = open(choice(list), 'rb')
    await bot.send_photo(message.chat.id, photo=photo)

@dp.message_handler(commands=['quiz'])
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

@dp.callback_query_handler(lambda call: call.data == 'button_1')
async def quiz_2(call: types.CallbackQuery):
    question = "Asil is got?"
    answers = ['Esen', 'Marlen', 'Aitegin']
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        open_period=10,
        correct_option_id= 1,
        is_anonymous=True,
        explanation='Of course!!!',
        explanation_parse_mode=ParseMode.MARKDOWN_V2
    )

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        await bot.send_message(message.chat.id, int(message.text)**2)
    else:
        await bot.send_message(message.chat.id, message.text)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)