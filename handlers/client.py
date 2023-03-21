from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import client_kb
from aiogram.dispatcher.storage import FSMContext
from data_base.sqlite_db import sql_add_command, sql_delete_row
import random


id_word = 0

class FSMClient(StatesGroup):
    id_user = State()
    id_word = State()
    en_word = State()
    ru_word = State()
    discribe = State()

async def command_start(message: types.Message):
    # print(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Привет, это бот по изучению английского. Следуй ниже по кнопкам', reply_markup=client_kb)

async def cm_start(message: types.Message, state: FSMContext):
    await FSMClient.en_word.set()
    async with state.proxy() as data:
        data['id_user'] = str(message.from_user.id)
    await message.reply('Напиши сообщение по следующему образцу:\n<Слово на английском>\n<Перевод>\n<Описание или "-" "_" "Без описания">\nВведи "отмена" если передумал')

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

async def add_enword(message: types.Message, state: FSMContext):
    global words
    words = str(message.text).split('\n')
    if len(words) == 2:
        words.append('-')

    async with state.proxy() as data:
        enword = words[0][0].upper() + words[0][1:].lower()
        data['enword'] = enword
    await FSMClient.next()

    async with state.proxy() as data:
        ruword = words[1][0].upper() + words[1][1:].lower()
        data['ruword'] = ruword
    await FSMClient.next()
    
    global id_word

    # global id_word
    async with state.proxy() as data:
        data['description'] = words[2]
        data['id_word'] = id_word
        id_word += 1
    await sql_add_command(state)
    await state.finish()

# async def add_ruword(state: FSMContext):
#     async with state.proxy() as data:
#         data['ruword'] = words[1]
#     await FSMClient.next()

# async def add_discribe(state: FSMContext):
#     global id_word
#     async with state.proxy() as data:
#         data['description'] = words[2]
#         data['id_word'] = str(id_word)
#         id_word += 1
#     await sql_add_command(state)
#     await state.finish()
#     await bot.send_message('Добавилось')

class FSMClientDel(StatesGroup):
    enword_del = State()

async def start_del_word(message: types.Message):
    await FSMClientDel.enword_del.set()
    await message.reply('Введи слово на английском, чтобы удалить его')

async def finish_del_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delword'] = message.text 
    await sql_delete_row(state)
    await state.finish()
    await message.reply('Слово удалено')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(cm_start, commands=['Добавить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(add_enword, state=FSMClient.en_word)
    # dp.register_message_handler(add_ruword, state=FSMClient.ru_word)
    # dp.register_message_handler(add_discribe, state=FSMClient.discribe)
    dp.register_message_handler(start_del_word, commands=['Удалить'], state=None)
    dp.register_message_handler(finish_del_word, state=FSMClientDel.enword_del)