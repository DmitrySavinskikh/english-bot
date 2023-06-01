from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Отмена_и_выход')
b2 = KeyboardButton('/Добавить_слово')
b3 = KeyboardButton('/Удалить_последнее_слово')
b4 = KeyboardButton('/Удалить_конкретное_слово')

client_adding_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

client_adding_kb.row(b1, b2, b3, b4)

b1_2 = KeyboardButton('/Отмена_и_выход')

client_adding_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

client_adding_kb2.row(b1_2)