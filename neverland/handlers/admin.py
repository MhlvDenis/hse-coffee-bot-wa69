from aiogram import types, Dispatcher
from create_bot import dp, bot
from database import sqlite_db


@dp.message_handler(commands=['allsee'])
async def show_all_users(message: types.Message):
    if sqlite_db.is_admin(message.from_user.id):
        result = await sqlite_db.sql_read()
        if result:
            for ret in result:
                if ret:
                    await bot.send_photo(message.from_user.id, ret[0],
                                         f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}\nUsername: {ret[5]}')


@dp.message_handler(commands=['allhashtags'])
async def show_all_hashtags(message: types.Message):
    if sqlite_db.is_admin(message.from_user.id):
        hashtags = await sqlite_db.get_sorted_hashtags()
        if hashtags:
            await bot.send_message(message.from_user.id, ', '.join(hashtags))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(show_all_users, commands=['allsee'])
    dp.register_message_handler(show_all_hashtags, commands=['allhashtags'])
