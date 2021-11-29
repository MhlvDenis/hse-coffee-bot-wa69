from aiogram import types, Dispatcher
from create_bot import dp, bot
from database import sqlite_db


@dp.message_handler(commands=['Посмотреть_всех'])
async def show_all(message: types.Message):
    if sqlite_db.is_admin(message.from_user.id):
        await sqlite_db.sql_read(message.from_user.id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(show_all, commands=['Посмотреть_всех'])
