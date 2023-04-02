from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b0 = KeyboardButton('/Знаю')
b1 = KeyboardButton('/Не_знаю')

student_eng_rus_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

student_eng_rus_kb.row(b0, b1)

