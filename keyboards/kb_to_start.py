from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button = KeyboardButton('/start')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_kb.add(button)
