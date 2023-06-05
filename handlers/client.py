from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from keyboards import client_kb, start_kb
from aiogram.dispatcher.storage import FSMContext
from data_base.sqlite_db import sql_delete_row
from data_base import sqlite_db


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, это бот по изучению английского. Следуй ниже по кнопкам', reply_markup=client_kb)
    sqlite_db.sql_start(message.from_user.id)

class FSMClientDel(StatesGroup):
    enword_del = State()

async def start_del_word(message: types.Message):
    if await sqlite_db.if_not_empty(message.from_user.id):
        await FSMClientDel.enword_del.set()
        await bot.send_message(message.from_user.id, 'Введи слово на английском, чтобы удалить его', reply_markup=start_kb)
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст', reply_markup=start_kb)

async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'OK', reply_markup=client_kb)

async def finish_del_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delword'] = message.text 
    await sql_delete_row(state)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Слово удалено', reply_markup=client_kb)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(start_del_word, commands=['Удалить'], state=None)
    dp.register_message_handler(cancel_handler, commands=['start'], state='*')
    dp.register_message_handler(finish_del_word, state=FSMClientDel.enword_del)