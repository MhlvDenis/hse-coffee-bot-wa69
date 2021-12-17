from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_make_profile, kb_user, kb_admin
from database import sqlite_db
from config import HELP_DOC


@dp.message_handler(commands=['start'])
async def bot_start_work(message: types.Message):
    if not await sqlite_db.sql_user_exists(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Привет! Давай сделаем для тебя профиль', reply_markup=kb_make_profile)
    else:
        await bot.send_message(message.from_user.id, 'Хей, а ты ведь уже зарегистрирован!\nВот твой профиль:',
                               reply_markup=kb_admin if sqlite_db.is_admin(message.from_user.id) else kb_user)
        await sqlite_db.sql_get_profile(message.from_user.id)


@dp.message_handler(commands=['help'])
async def get_help(message: types.Message):
    await message.reply(HELP_DOC)


@dp.message_handler(commands=['profile'])
async def get_profile(message: types.Message):
    ret = await sqlite_db.sql_get_profile(message.from_user.id)
    await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}')


@dp.message_handler(commands=['companion'])
async def get_predict(message: types.Message):
    predicts = await sqlite_db.sql_predict_shuffle(message.from_user.id)
    if predicts:
        for predict_id in predicts:
            ret = await sqlite_db.sql_another_profile(predict_id)
            await bot.send_photo(message.from_user.id, ret[0],
                                 f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}\nUsername: @{ret[5]}')
    else:
        await bot.send_message(message.from_user.id, 'Пока никого не нашел :(')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(bot_start_work, commands=['start'])
    dp.register_message_handler(get_help, commands=['help'])
    dp.register_message_handler(get_profile, commands=['profile'])
    dp.register_message_handler(get_predict, commands=['companion'])
