from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot('6154232003:AAEMgc3FgMLAIyMNchllRJuDd2kf9QNTU24')
dp = Dispatcher(bot, storage=storage)
