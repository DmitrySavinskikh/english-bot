from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Добавить')
b2 = KeyboardButton('/Учить')
b3 = KeyboardButton('/Удалить')

client_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

client_kb.row(b1, b2, b3)