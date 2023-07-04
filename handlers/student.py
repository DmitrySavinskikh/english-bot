from aiogram.dispatcher import Dispatcher
from create_bot import bot
from keyboards import student_kb
from aiogram import types
from data_base import sqlite_db


async def start_mode_student(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ты вошёл в режим обучения, следуй по кнопкам ниже', reply_markup=student_kb)

async def my_dict(message : types.Message):
    if await sqlite_db.if_not_empty(message.from_user.id):
        await sqlite_db.sql_read_all(message, message.from_user.id)
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст')

def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(start_mode_student, commands=['Режим_обучения'])
    dp.register_message_handler(my_dict, commands=['Мой_словарь'])