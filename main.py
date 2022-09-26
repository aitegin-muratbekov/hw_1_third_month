import asyncio
import logging
from aiogram.utils import executor
from handlers import extra, callback, client, fsmAdminMenu, notifications
from config import bot, dp
from database.bot_db import sql_create

async def on_startup(_):
    sql_create()
    asyncio.create_task(notifications.scheduler())

notifications.register_handlers_notification(dp)
client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
fsmAdminMenu.register_handlers_fsm_admin(dp)
extra.register_handler_extra(dp)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

