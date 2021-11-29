import sqlite3 as sq
import re
import random
from config import ADMIN_ID
from create_bot import bot


def is_admin(usr_id):
    return usr_id == ADMIN_ID


def sql_start():
    global base, cur
    base = sq.connect('users.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS users(photo TEXT, name TEXT, description TEXT, hashtags TEXT, id INT PRIMARY KEY, username TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(usr_id):
    for ret in cur.execute('SELECT * FROM users').fetchall():
        await bot.send_photo(usr_id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}\nUsername: {ret[5]}')


async def sql_user_exists(usr_id):
    return cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone() is not None


async def sql_get_profile(usr_id):
    if await sql_user_exists(usr_id):
        ret = cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone()
        await bot.send_photo(usr_id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}')


async def sql_another_profile(host_id, usr_id):
    if await sql_user_exists(usr_id):
        ret = cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone()
        await bot.send_photo(host_id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}\nUsername: @{ret[5]}')


async def sql_predict_shuffle(usr_id):
    if await sql_user_exists(usr_id):
        cur_usr = cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone()
        cur_id = cur_usr[4]
        cur_hashtags = set(_ for _ in re.findall(r"#(\w+)", cur_usr[3]))
        predict_users = []
        for ret in cur.execute('SELECT * FROM users WHERE id != ?', (cur_id, )).fetchall():
            predict_hashtags = set(_ for _ in re.findall(r"#(\w+)", ret[3]))
            predict_users.append([len(cur_hashtags.intersection(predict_hashtags)), ret[4]])
        for usr in predict_users:
            usr[0] += random.randint(0, 4)
        predict_users.sort(reverse=True)
        return [_[1] for _ in predict_users[:2]]
