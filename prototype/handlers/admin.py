from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from ClassDB import class_db
from bot import dp


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


class FSMAdminDELETE(StatesGroup):
    name = State()
    price = State()


# @dp.message_handler(commands='Delete', state=None)
async def admin_start_delete(message: types.Message):
    await FSMAdminDELETE.name.set()
    await message.reply('Please write name pizza.')


# @dp.message_handler(state=FSMAdminDELETE.name)
async def write_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdminDELETE.next()
    await message.reply("Please write price pizza.")


# @dp.message_handler(state=FSMAdminDELETE.price)
async def write_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    async with state.proxy() as data:
        class_db.Database('./Database/database.db').DELETE(data['name'], data['price'])
        await message.reply('Pizza deleted successfully.')
    await state.finish()


# @dp.message_handler(commands='Add', state=None)
async def admin_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Upload a photo.')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Please write name pizza.')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Please write description pizza.")


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Please write price pizza.")


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    async with state.proxy() as data:
        class_db.Database('./Database/database.db').ADD(data['photo'], data['name'], data['description'], data['price'])
        await message.reply('Pizza added successfully.')
    await state.finish()


async def stop_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return f'Is non add'
    await state.finish()
    await message.reply('OK!')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands='Add', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(stop_state, state="*", commands='stop')
    dp.register_message_handler(stop_state, Text(equals='stop', ignore_case=True), state="*")
    dp.register_message_handler(admin_start_delete, commands='Delete', state=None)
    dp.register_message_handler(write_name, state=FSMAdminDELETE.name)
    dp.register_message_handler(write_price, state=FSMAdminDELETE.price)

