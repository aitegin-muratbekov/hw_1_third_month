from aiogram import Bot, Dispatcher
from decouple import config
TOKEN = config("TOKEN")

ADMINS = [1746350842]
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)