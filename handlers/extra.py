from aiogram import types, Dispatcher
from config import bot, dp, ADMINS
from random import choice


async def echo(message: types.Message):
    emoji = ["⚽️", "🏀", "🎲", "🎳", "🎯", "🎰"]
    if message.text == "game":
        if message.chat.type != "private":
            if not message.from_user.id in ADMINS:
                await message.reply("ты не мой босс!")
            else:
                await bot.send_dice(message.chat.id, emoji=choice(emoji))
        else:
            await message.reply("Пиши в группу")
    else:
        if message.text.isdigit():
            await bot.send_message(message.chat.id, int(message.text) ** 2)
        else:
            await bot.send_message(message.chat.id, message.text)


def register_handler_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
