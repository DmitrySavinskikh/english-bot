from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from keyboards import client_teacher_kb, client_teacher_kb2
from aiogram.dispatcher.storage import FSMContext
from data_base import sqlite_db


pupil_id = ''
words_this_session = []

class FSMTeacherID(StatesGroup):
    id = State()

async def initialization(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ты вошёл в режим учителя', reply_markup=client_teacher_kb)

async def start_input_id(message: types.Message):
    await FSMTeacherID.id.set()
    await bot.send_message(message.from_user.id, 'Введи id пользователя, которого ты будешь учить', reply_markup=client_teacher_kb)
    

async def finish_input_id(message: types.Message, state:FSMContext):
    global pupil_id
    async with state.proxy() as data:
        data['pupil_id'] = message.text
    pupil_id = message.text
    await state.finish()
    if await sqlite_db.if_not_empty(pupil_id):
        sqlite_db.sql_start(pupil_id)
        await bot.send_message(message.from_user.id, 'Словарь ' + pupil_id + ' подключён, теперь ты работаешь с его словарём.\nДля доступа к своему словарю введи /start', reply_markup=client_teacher_kb)
    else:
        await bot.send_message(message.from_user.id, 'Словарь этого юзера пуст', reply_markup=client_teacher_kb)
        sqlite_db.sql_start(pupil_id)
        await bot.send_message(message.from_user.id, 'Словарь создан и подключён', reply_markup=client_teacher_kb)


class FSMTeacher_adding(StatesGroup):
    id_word = State()
    en_word = State()
    ru_word = State()
    discribe = State()


async def start_add_word(message: types.Message):
    await FSMTeacher_adding.en_word.set()
    await bot.send_message(message.from_user.id, 'Напиши сообщение по следующему образцу:\n<Слово на английском>\n<Перевод>\n<Описание или "-" "_" "Без описания">', reply_markup=client_teacher_kb2)


async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'OK', reply_markup=client_teacher_kb)

async def add_enword(message: types.Message, state: FSMContext):
    global words
    words = str(message.text).split('\n')
    if len(words) < 3:
        await bot.send_message(message.from_user.id, 'Неверно заполнена форма', reply_markup=client_teacher_kb2)
        await start_add_word(message)
        return

    async with state.proxy() as data:
        enword = words[0][0].upper() + words[0][1:].lower()
        data['enword'] = enword
    await FSMTeacher_adding.next()

    async with state.proxy() as data:
        ruword = words[1][0].upper() + words[1][1:].lower()
        data['ruword'] = ruword
    await FSMTeacher_adding.next()

    async with state.proxy() as data:
        data['description'] = words[2]
        data['id_word'] = await sqlite_db.max_id_word() + 1
    await sqlite_db.sql_add_command(state)
    await state.finish()
    words_this_session.append(enword)
    await bot.send_message(message.from_user.id, 'Слово "'+words_this_session[-1]+'" добавлено в словарь', reply_markup=client_teacher_kb2)
    await start_add_word(message)

async def del_prev_word(message: types.Message):
    word = await sqlite_db.sql_del_prev_row()
    await bot.send_message(message.from_user.id, 'Слово "' + str(word) + '" удалено', reply_markup=client_teacher_kb2)


class FSMTeacher_del(StatesGroup):
    enword = State()


async def del_specific_word(message: types.Message):
    if await sqlite_db.if_not_empty(pupil_id):
        await FSMTeacher_del.enword.set()
        await message.reply('Введи слово на английском, чтобы удалить его', reply_markup=client_teacher_kb2)
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст', reply_markup=client_teacher_kb)

async def del_specific_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        words = message.text
        words = words[0].upper() + words[1:].lower()
        data['enword'] = words
    await sqlite_db.sql_delete_row(state)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Слово удалено', reply_markup=client_teacher_kb)

async def user_dict(message: types.Message):
    if await sqlite_db.if_not_empty(pupil_id):
        await sqlite_db.sql_read_all(message, pupil_id)
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст')

def register_handlers_client_teacher(dp: Dispatcher):
    dp.register_message_handler(initialization, commands=['Режим_учителя'])
    dp.register_message_handler(start_input_id, commands=['Ввести_id'], state=None)
    dp.register_message_handler(finish_input_id, state=FSMTeacherID.id)
    dp.register_message_handler(start_add_word, commands=['Добавить_слово_юзеру'], state=None)
    dp.register_message_handler(cancel_handler, commands=['Отмена_и_выход'], state='*')
    dp.register_message_handler(add_enword, state=FSMTeacher_adding.en_word)
    dp.register_message_handler(del_prev_word, commands=['Удалить_последнее_слово_юзеру'], state=None)
    dp.register_message_handler(del_specific_word, commands=['Удалить_конкретное_слово_юзеру'], state=None)
    dp.register_message_handler(del_specific_finish, state=FSMTeacher_del.enword)
    dp.register_message_handler(user_dict, commands=['Посмотреть_словарь_юзера'])