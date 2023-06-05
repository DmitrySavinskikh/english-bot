from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b0 = KeyboardButton('/Учить')
b1 = KeyboardButton('/Мой_словарь')
b2 = KeyboardButton('/ру_ен')
b3 = KeyboardButton('/ен_ру')
b4 = KeyboardButton('/start')

student_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

student_kb.row(b1, b2, b3, b4)

