import sqlite3 as sq
from create_bot import bot
import random
# from handlers.client import id_word


def sql_start():
    global base, cur
    base = sq.connect('dictionary.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS dictionary(id_user TEXT, en_word TEXT, ru_word TEXT, describe TEXT, id_word INTEGER, repeats INTEGER)')
    # base.execute('INSERT INTO dictionary(repeats) VALUES (10)')
    base.commit()

async def if_not_empty(id_user):
    # print(len(cur.execute('SELECT * FROM dictionary').fetchall()))
    if len(cur.execute('SELECT * FROM dictionary WHERE id_user = (?)', [id_user]).fetchall()) == 0:
        return False
    else:
        return True

async def sql_add_command(state):
    async with state.proxy() as data:
        # print(data)
        # enword = tuple(data.values())[1]
        cur.execute('INSERT INTO dictionary VALUES (?, ?, ?, ?, ?, 10)', tuple(data.values()))
        base.commit()
    
async def sql_read(message, id_user):
    if await if_not_empty(id_user):
        for ret in cur.execute('SELECT * FROM dictionary WHERE id_user = (?)', [id_user]).fetchall():
            await bot.send_message(message.from_user.id, f'{ret[1], ret[2]}\nописание: {ret[3]}')
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
        WITH user_dictionary AS (SELECT * FROM dictionary WHERE id_user = ?)
        SELECT * FROM user_dictionary WHERE repeats = (SELECT MAX(repeats) FROM user_dictionary) ORDER BY RANDOM() LIMIT 1
        ''', [id_user]).fetchone()

        base.commit()
        return res[1], res[2], res[3]

async def minus_one_repeat(id_user, enword):
    if await if_not_empty(id_user):
        # print(enword)
        repeats = cur.execute('''
        WITH user_dictionary AS (SELECT * FROM dictionary WHERE id_user = ?)
        SELECT * FROM user_dictionary WHERE repeats = (SELECT MAX(repeats) FROM user_dictionary) ORDER BY RANDOM() LIMIT 1
        ''', [id_user]).fetchone()[5]
        # print(repeats)

        cur.execute('UPDATE dictionary SET repeats = ? WHERE en_word = ? AND id_user = ?', [repeats - 1, enword, id_user])
        res = cur.execute('SELECT * FROM dictionary WHERE en_word = ?', [enword]).fetchall()
        # print(res)

        repeats_after = cur.execute('''SELECT * FROM dictionary WHERE id_user = ? AND en_word = ?''', [id_user, enword]).fetchone()[5]
        # print(repeats_after)
        base.commit()
        return repeats_after