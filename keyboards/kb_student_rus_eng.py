from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Знаю')
b0 = KeyboardButton('/Не_знаю')
b2 = KeyboardButton('/start')
b3 = KeyboardButton('/letsgo')

student_rus_eng_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

student_rus_eng_kb.row(b0, b1).row(b2, b3)

