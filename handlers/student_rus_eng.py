from aiogram.dispatcher import Dispatcher
from create_bot import bot
from keyboards import student_rus_eng_kb
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from data_base import sqlite_db


async def start_mode_student(message: types.Message):
    await bot.send_message(message.from_user.id, "Ты вошёл в режим обучения 'ру_ен'", reply_markup=student_rus_eng_kb)

class FSMStudent_ruen(StatesGroup):
    wait_reply = State()


async def send_random_ruword(message: types.Message):
    global enword, description, ruword
    if await sqlite_db.if_not_empty(message.from_user.id):
        set_data = await sqlite_db.sql_take_set(message.from_user.id)
        await bot.send_message(message.from_user.id, set_data[1], reply_markup=student_rus_eng_kb)
        ruword = set_data[1]
        enword = set_data[0]
        description = set_data[2]
        return set_data[1]
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст')

async def learn_ru_en_word(message: types.Message, state: FSMContext):
    if await sqlite_db.if_not_empty(message.from_user.id):
        await FSMStudent_ruen.wait_reply.set()
        await bot.send_message(message.from_user.id, "let's go", reply_markup=student_rus_eng_kb)

        async with state.proxy() as data:
            expected = await send_random_ruword(message)
            data['expected'] = expected
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст')

async def get_word_ruen(message: types.Message, state: FSMContext):
    if await sqlite_db.if_not_empty(message.from_user.id):
        message_user = message.text
        if message_user == 'выйти':
            await bot.send_message(message.from_user.id, 'OK')
            await state.finish()
            return

        async with state.proxy() as data:
            if message_user.lower() == '/знаю':
                repeats = await sqlite_db.minus_one_repeat(message.from_user.id, enword)
                if repeats == 0:
                    await bot.send_message(message.from_user.id, 'Ты выучил это слово!')
                    await sqlite_db.sql_delete_row(state)
                else:
                    await bot.send_message(message.from_user.id, f'До выучивания осталось {repeats} повторений')
            elif message_user.lower() == '/не_знаю':
                list_ = await sqlite_db.read_word_rus(ruword)
                await bot.send_message(message.from_user.id, f'{list_[0], list_[1]}\nописание: {list_[2]}')
            else:
                await bot.send_message(message.from_user.id, "Введи 'знаю' или 'не знаю'")
            expected = await send_random_ruword(message)
            data['expected'] = expected
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст')

def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(start_mode_student, commands=['ру_ен'])
    dp.register_message_handler(learn_ru_en_word, commands=['letsgo'])
    dp.register_message_handler(get_word_ruen, state=FSMStudent_ruen.wait_reply)