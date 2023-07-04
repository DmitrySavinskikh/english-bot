from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from keyboards import client_adding_kb, client_kb, client_adding_kb2
from aiogram.dispatcher.storage import FSMContext
from data_base import sqlite_db

words_this_session = []

async def sigh_in(message: types.Message):
    await bot.send_message(message.from_user.id, "Ты вошёл в режим добавления новых слов, в случае ошибки можно сразу удалить слово", reply_markup=client_adding_kb)

class FSMClient_adding(StatesGroup):
    id_word = State()
    en_word = State()
    ru_word = State()
    discribe = State()
    
async def cm_start(message: types.Message):
    await FSMClient_adding.en_word.set()
    await bot.send_message(message.from_user.id, 'Напиши сообщение по следующему образцу:\n<Слово на английском>\n<Перевод>\n<Описание или "-" "_" "Без описания">', reply_markup=client_adding_kb2)

async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'OK', reply_markup=client_kb)

async def add_enword(message: types.Message, state: FSMContext):
    global words
    words = str(message.text).split('\n')
    if len(words) < 3:
        await bot.send_message(message.from_user.id, 'Неверно заполнена форма')
        await cm_start(message)
        return

    async with state.proxy() as data:
        enword = words[0][0].upper() + words[0][1:].lower()
        data['enword'] = enword
    await FSMClient_adding.next()

    async with state.proxy() as data:
        ruword = words[1][0].upper() + words[1][1:].lower()
        data['ruword'] = ruword
    await FSMClient_adding.next()

    async with state.proxy() as data:
        data['description'] = words[2]
        data['id_word'] = await sqlite_db.max_id_word() + 1
    await sqlite_db.sql_add_command(state)
    await state.finish()
    words_this_session.append(enword)
    await bot.send_message(message.from_user.id, 'Слово "'+words_this_session[-1]+'" добавлено в словарь')
    await cm_start(message)

async def del_prev_word(message: types.Message):
    word = await sqlite_db.sql_del_prev_row()
    await bot.send_message(message.from_user.id, 'Слово "' + str(word) + '" удалено', reply_markup=client_adding_kb)

class FSMClient_del(StatesGroup):
    enword = State()


async def del_specific_word(message: types.Message):
    if await sqlite_db.if_not_empty(message.from_user.id):
        await FSMClient_del.enword.set()
        await message.reply('Введи слово на английском, чтобы удалить его')
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст', reply_markup=client_adding_kb)

async def del_specific_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        words = message.text
        words = words[0].upper() + words[1:].lower()
        data['enword'] = words
    await sqlite_db.sql_delete_row(state)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Слово удалено', reply_markup=client_adding_kb)


def register_handlers_client_adding(dp: Dispatcher):
    dp.register_message_handler(sigh_in, commands=['Режим_добавить'], state=None)
    dp.register_message_handler(cm_start, commands=['Добавить_слово'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, commands=['Отмена_и_выход'], state='*')
    dp.register_message_handler(add_enword, state=FSMClient_adding.en_word)
    dp.register_message_handler(del_prev_word, commands=['Удалить_последнее_слово'], state=None)
    dp.register_message_handler(del_specific_word, commands=['Удалить_конкретное_слово'], state=None)
    dp.register_message_handler(del_specific_finish, state=FSMClient_del.enword)