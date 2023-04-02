from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b0 = KeyboardButton('/Учить')
b1 = KeyboardButton('/Мой_словарь')
b2 = KeyboardButton('/рус_англ')
b3 = KeyboardButton('/ен_ру')

student_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

student_kb.row(b1, b2, b3)

