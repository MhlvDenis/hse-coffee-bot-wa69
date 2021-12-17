import sqlite3 as sq
import re
import random
from collections import Counter
from config import ADMIN_ID
from create_bot import bot


def is_admin(usr_id):
    return usr_id == ADMIN_ID


def sql_start():
    global users, users_cur, hashtags, hashtags_cur
    users = sq.connect('users.db')
    hashtags = sq.connect('hashtags.db')
    users_cur = users.cursor()
    hashtags_cur = hashtags.cursor()
    if users:
        print('Data users connected OK')
    if hashtags:
        print('Data hashtags connected OK')
    users.execute('CREATE TABLE IF NOT EXISTS users(photo TEXT, name TEXT, description TEXT, hashtags TEXT, id INT PRIMARY KEY, username TEXT)')
    users.commit()
    hashtags.execute('CREATE TABLE IF NOT EXISTS hashtags(hashtags TEXT, id INT PRIMARY KEY)')
    hashtags.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        users_cur.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        users.commit()
        hashtags_cur.execute('INSERT OR IGNORE INTO hashtags VALUES (?, ?)', (data['hashtags'], data['id'], ))
        hashtags.commit()


async def sql_read():
    return users_cur.execute('SELECT * FROM users').fetchall()


async def sql_user_exists(usr_id):
    return users_cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone() is not None


async def sql_get_profile(usr_id):
    if await sql_user_exists(usr_id):
        return users_cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone()


async def sql_another_profile(usr_id):
    if await sql_user_exists(usr_id):
        return users_cur.execute('SELECT * FROM users WHERE id == ?', (usr_id, )).fetchone()


async def sql_predict_shuffle(usr_id):
    if await sql_user_exists(usr_id):
        cur_usr = hashtags_cur.execute('SELECT * FROM hashtags WHERE id == ?', (usr_id, )).fetchone()
        cur_id = cur_usr[1]
        cur_hashtags = set(_ for _ in re.findall(r"#(\w+)", cur_usr[0]))
        predict_users = []
        for ret in hashtags_cur.execute('SELECT * FROM hashtags WHERE id != ?', (cur_id, )).fetchall():
            predict_hashtags = set(_ for _ in re.findall(r"#(\w+)", ret[0]))
            predict_users.append([len(cur_hashtags.intersection(predict_hashtags)), ret[1]])
        for usr in predict_users:
            usr[0] += random.randint(0, 4)
        predict_users.sort(reverse=True)
        return [_[1] for _ in predict_users[:2]]


async def get_sorted_hashtags():
    hashtags_list = []
    for ret in hashtags_cur.execute('SELECT * FROM hashtags').fetchall():
        hashtags_list += re.findall(r"#(\w+)", ret[0])
    return [_[0] for _ in Counter(hashtags_list).most_common()]


async def get_popular_hashtags():
    return get_sorted_hashtags()[:5]


async def set_field(state):
    async with state.proxy() as data:
        users_cur.execute('UPDATE users SET ' + data['field'] + ' = ? WHERE id = ?', (data['content'], data['id'], ))
        users.commit()
