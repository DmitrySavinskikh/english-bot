from aiogram.utils import executor
from create_bot import dp
from handlers import client, student, student_eng_rus, student_rus_eng
from data_base import sqlite_db


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()

client.register_handlers_client(dp)
student.register_handlers_student(dp)
student_eng_rus.register_handlers_student(dp)
student_rus_eng.register_handlers_student(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
