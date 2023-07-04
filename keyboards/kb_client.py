from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Режим_добавить')
b2 = KeyboardButton('/Режим_обучения')
b3 = KeyboardButton('/Режим_удаления')
b4 = KeyboardButton('/Режим_учителя')

client_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

client_kb.row(b1, b2, b3).add(b4)