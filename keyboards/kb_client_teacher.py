from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Добавить_слово_юзеру')
b2 = KeyboardButton('/Удалить_последнее_слово_юзеру')
b3 = KeyboardButton('/Удалить_конкретное_слово_юзеру')
b4 = KeyboardButton('/Посмотреть_словарь_юзера')
b0 = KeyboardButton('/Ввести_id')
b_exit = KeyboardButton('/Отмена_и_выход')

client_teacher_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

client_teacher_kb.add(b1, b2, b3, b4, b0, b_exit)

b1_2 = KeyboardButton('/Отмена_и_выход')

client_teacher_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

client_teacher_kb2.add(b1_2)