import logging
from aiogram.utils import executor
from handlers import extra, callback, client
from config import bot, dp


client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
extra.register_handler_extra(dp)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)

