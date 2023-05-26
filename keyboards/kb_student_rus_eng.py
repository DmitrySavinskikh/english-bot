from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b0 = KeyboardButton('/Знаю')
b1 = KeyboardButton('/Не_знаю')

student_rus_eng_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

student_rus_eng_kb.row(b0, b1)

