from config import dp, bot
from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

async def quiz_2(call: types.CallbackQuery):
    question = "Asil is got?"
    answers = ['Esen', 'Marlen', 'Aitegin']
    markup = InlineKeyboardMarkup()
    button_2 = InlineKeyboardButton('NEXT', callback_data='button_2')
    markup.add(button_2)
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        open_period=10,
        correct_option_id= 1,
        is_anonymous=True,
        explanation='Of course!!!',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup = markup,

    )
async def quiz_3(call: types.CallbackQuery):
    question = "Asil is really got?"
    answers = ['Year bro', 'No no no']

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        open_period=10,
        correct_option_id=1,
        is_anonymous=True,
        explanation='Of course!!!',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,

    )


def register_handlers_callback(dp:Dispatcher):
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == 'button_1')
    dp.register_callback_query_handler(quiz_3, lambda call: call.data == 'button_2')