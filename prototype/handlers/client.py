from aiogram import types, Dispatcher
from ClassDB import class_db
from bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from ClassID import class_id


class FSMClient(StatesGroup):
    caption = State()
    username = State()
    address = State()
    number_phone = State()


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_menu = types.KeyboardButton('Menu')
    button_work_time = types.KeyboardButton('Work time')
    button_information = types.KeyboardButton('Information')
    keyboard.add(button_menu, button_work_time, button_information)
    await message.answer(f'Hello, {message.from_user.first_name}. Pizza Paradise welcomes you!', reply_markup=keyboard)


# @dp.callback_query_handlers(text='order')
async def order(call: types.CallbackQuery, state: FSMContext):
    await FSMClient.username.set()
    async with state.proxy() as data:
        data['caption'] = call.message.caption
    await call.message.reply('Please write yor name.')


# @dp.message_handler(state=FSMClient.username)
async def write_user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMClient.next()
    await message.reply("Please write your address.")


# @dp.message_handler(state=FSMClient.address)
async def write_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await FSMClient.next()
    await message.reply("Please write your number phone.")


# @dp.message_handler(state=FSMClient.number_phone)
async def write_number_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_phone'] = message.text
    id_order = class_id.ID().appropriation_id()
    async with state.proxy() as data:
        text = f"Name: {data['username']}\nAddress: {data['address']}\nPhone number: {data['number_phone']}\n{data['caption']}\nOrder ID: {id_order}"
        await message.answer(f'Order ID: {id_order}')
        await bot.send_message(-977325025, text)
    await state.finish()


async def callback(message: types.Message):
    if message.text == 'Menu':
        keyboard = types.InlineKeyboardMarkup()
        button_order = types.InlineKeyboardButton(text='Order', callback_data='order')
        keyboard.add(button_order)
        menu = class_db.Database('./Database/database.db').MENU_DISPLAY()
        for position in menu:
            caption = f'Name pizza: {position[1]}\nDescription: {position[2]}\nPrice: {position[3]}$'
            await bot.send_photo(message.from_user.id, photo=position[0], caption=caption, reply_markup=keyboard)
    elif message.text == 'Work time':
        await message.answer(''''
        Monday: 10:00 AM - 9:00 PM\n
        Tuesday: 10:00 AM - 9:00 PM\n
        Wednesday: 10:00 AM - 9:00 PM\n
        Thursday: 10:00 AM - 9:00 PM\n
        Friday: 10:00 AM - 10:00 PM\n
        Saturday: 10:00 AM - 10:00 PM\n
        Sunday: Closed\n\'\
        ''')
    elif message.text == 'Information':
        await message.answer(''''
        Pizza Paradise\n
        Address: 123 Main Street, City\n
        Phone: +38(045)-67-85-398\n
        Email: info@pizzaparadise.com\n\'\
        ''')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(callback)
    dp.register_callback_query_handler(order, text='order', state=None)
    dp.register_message_handler(write_user_name, state=FSMClient.username)
    dp.register_message_handler(write_address, state=FSMClient.address)
    dp.register_message_handler(write_number_phone, state=FSMClient.number_phone)

