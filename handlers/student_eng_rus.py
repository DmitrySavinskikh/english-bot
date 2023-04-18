from aiogram.dispatcher import Dispatcher
from create_bot import bot
from keyboards import student_eng_rus_kb
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from data_base import sqlite_db


async def start_mode_student(message: types.Message):
    await message.reply("Ты вошёл в режим обучения 'ен_ру', для выхода введи '/start'.\nЕсли ты готов, то пиши '/letsgo'", reply_markup=student_eng_rus_kb)

class FSMStudent_enru(StatesGroup):
    wait_reply = State()

ruword = ''
description = ''
async def send_random_enword(message: types.Message):
    global ruword, description, enword
    if await sqlite_db.if_not_empty(message.from_user.id):
        set_data = await sqlite_db.sql_take_set(message.from_user.id)
        # print(set_data)
        await message.reply(set_data[0])
        ruword = set_data[1]
        enword = set_data[0]
        description = set_data[2]
        return set_data[1]

async def learn_en_ru_word(message: types.Message, state: FSMContext):
    if await sqlite_db.if_not_empty(message.from_user.id):
        await FSMStudent_enru.wait_reply.set()
        await message.reply("let's go, пиши 'знаю' или 'не знаю'\nPS: если закончил, напиши 'выйти'")

        async with state.proxy() as data:
            expected = await send_random_enword(message)
            data['expected'] = expected

async def get_word_enru(message: types.Message, state: FSMContext):
    if await sqlite_db.if_not_empty(message.from_user.id):
        message_user = message.text
        if message_user.lower() == 'выйти':
            await bot.send_message(message.from_user.id, 'OK')
            await state.finish()
            return

        async with state.proxy() as data:
            # print(message_user, data['expected'])
            if message_user.lower() == '/знаю':
                repeats = await sqlite_db.minus_one_repeat(message.from_user.id, enword)
                if repeats == 0:
                    await bot.send_message(message.from_user.id, 'Ты выучил это слово!')
                    await sqlite_db.sql_delete_row(state)
                else:
                    await bot.send_message(message.from_user.id, f'До выучивания осталось {repeats} повторений')
                    await bot.send_message(message.from_user.id, ruword)
                    stop_symbols = ['-', '_', 'без описания']
                    if description.lower() not in stop_symbols:
                        await bot.send_message(message.from_user.id, f'Описание: {description}')
            elif message_user.lower() == '/не_знаю':
                await bot.send_message(message.from_user.id, 'Окей, ошибки - наши лучшие друзья ;)')
                await bot.send_message(message.from_user.id, ruword)
            else:
                await bot.send_message(message.from_user.id, "Следуй по кнопкам снизу или напиши 'выйти', если хочешь сделать это")
            expected = await send_random_enword(message)
            data['expected'] = expected

def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(start_mode_student, commands=['ен_ру'])
    dp.register_message_handler(learn_en_ru_word, commands=["letsgo"])
    dp.register_message_handler(get_word_enru, state=FSMStudent_enru.wait_reply)