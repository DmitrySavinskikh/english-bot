from aiogram.utils import executor
from create_bot import dp
from handlers import client, student, student_eng_rus, student_rus_eng, client_adding


async def on_startup(_):
    print('Бот вышел в онлайн')

client.register_handlers_client(dp)
client_adding.register_handlers_client_adding(dp)
student.register_handlers_student(dp)
student_eng_rus.register_handlers_student(dp)
student_rus_eng.register_handlers_student(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
