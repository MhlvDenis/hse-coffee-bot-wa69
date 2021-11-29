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


@dp.message_handler(commands=['Мой_профиль'])
async def get_profile(message: types.Message):
    await sqlite_db.sql_get_profile(message.from_user.id)


@dp.message_handler(commands=['Найти_сокофейника'])
async def get_predict(message: types.Message):
    predicts = await sqlite_db.sql_predict_shuffle(message.from_user.id)
    for predict_id in predicts:
        await sqlite_db.sql_another_profile(message.from_user.id, predict_id)


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(bot_start_work, commands=['start'])
    dp.register_message_handler(get_profile, commands=['Мой_профиль'])
    dp.register_message_handler(get_predict, commands=['Найти_сокофейника'])
    dp.register_message_handler(get_help, commands=['help'])
