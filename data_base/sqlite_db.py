import sqlite3 as sq
from create_bot import bot
import random
# from handlers.client import id_word


def check_existence_db(id):
    try:
        name_db = str(id) + '.db'
        conn = sq.connect(name_db)
    except sq.Error:
        return False
    return True

def sql_start(id):
    global base, cur
    base = sq.connect(str(id) + '.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    query = 'CREATE TABLE IF NOT EXISTS ' + str('dictionary') + '(en_word TEXT, ru_word TEXT, describe TEXT, id_word INTEGER, repeats INTEGER)'
    base.execute(query)
    base.commit()


async def if_not_empty(id_user):
    if check_existence_db(id_user):
        if len(cur.execute('SELECT * FROM dictionary').fetchall()) == 0:
            return False
        else:
            return True
    else:
        return False

async def sql_add_command(state):
    async with state.proxy() as data:
        # print(data)
        # enword = tuple(data.values())[1]
        cur.execute('INSERT INTO dictionary VALUES (?, ?, ?, ?, 10)', tuple(data.values()))
        base.commit()
    
async def sql_read_all(message, id_user):
    if await if_not_empty(id_user):
        for ret in cur.execute('SELECT * FROM dictionary').fetchall():
            await bot.send_message(message.from_user.id, f'{ret[0], ret[1]}\nописание: {ret[2]}')
    else:
        await bot.send_message(message.from_user.id, 'Словарь пуст, нажми /start и добавь новые слова')

async def sql_delete_row(state):
    async with state.proxy() as data:
        cur.execute('DELETE FROM dictionary WHERE en_word = (?)', tuple(data.values()))
        base.commit()

# пробовал реализовать с подсчётом максимального кол-ва повторений
async def sql_take_set(id_user):
    if await if_not_empty(id_user):
        res = cur.execute('''
        SELECT * FROM dictionary WHERE repeats = (SELECT MAX(repeats) FROM dictionary) ORDER BY RANDOM() LIMIT 1
        ''').fetchone()

        base.commit()
        return res[0], res[1], res[2]

async def minus_one_repeat(id_user, enword):
    if await if_not_empty(id_user):
        repeats = cur.execute('''
        SELECT * FROM dictionary WHERE repeats = (SELECT MAX(repeats) FROM dictionary) ORDER BY RANDOM() LIMIT 1
        ''').fetchone()[4]

        cur.execute('UPDATE dictionary SET repeats = ? WHERE en_word = ?', [repeats - 1, enword])

        repeats_after = cur.execute('''SELECT * FROM dictionary WHERE en_word = ?''', [enword]).fetchone()[4]
        base.commit()
        return repeats_after