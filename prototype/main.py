from aiogram import executor
from bot import dp


def start_bot():
    print('Bot is running.')


from handlers import client, admin

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=start_bot())
