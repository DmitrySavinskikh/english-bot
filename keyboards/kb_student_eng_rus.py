from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b0 = KeyboardButton('/Знаю')
b1 = KeyboardButton('/Не_знаю')
b2 = KeyboardButton('/start')

student_eng_rus_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

student_eng_rus_kb.row(b0, b1).add(b2)

