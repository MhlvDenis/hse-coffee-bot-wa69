from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import kb_make_profile, kb_cancel_profile, kb_user, kb_admin
from database import sqlite_db


class FSMMakeForm(StatesGroup):
    photo = State()
    name = State()
    description = State()
    hashtags = State()


@dp.message_handler(commands=['Создать_профиль'], state=None)
async def start_make_form(message: types.Message):
    if not await sqlite_db.sql_user_exists(message.from_user.id):
        await FSMMakeForm.photo.set()
        await bot.send_message(message.from_user.id, 'Загрузи свою фотографию', reply_markup=kb_cancel_profile)
    else:
        await bot.send_message(message.from_user.id, 'Хей, а ты ведь уже зарегистрирован!\nВот твой профиль:',
                               reply_markup=kb_admin if sqlite_db.is_admin(message.from_user.id) else kb_user)
        await sqlite_db.sql_get_profile(message.from_user.id)


@dp.message_handler(state="*", commands=['Отмена'])
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Ok', reply_markup=kb_make_profile)


@dp.message_handler(content_types=['photo'], state=FSMMakeForm.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMMakeForm.next()
    await message.reply('Введи свое имя')


@dp.message_handler(state=FSMMakeForm.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMMakeForm.next()
    await message.reply('Опиши себя в паре предложений')


@dp.message_handler(state=FSMMakeForm.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMMakeForm.next()
    await message.reply('Напиши несколько хештегов, по которым я смогу подобрать тебе лучшего сокофейника')


@dp.message_handler(state=FSMMakeForm.hashtags)
async def load_hashtags(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hashtags'] = message.text
        data['id'] = message.from_user.id
        data['username'] = message.from_user.username
    await sqlite_db.sql_add_command(state)
    await bot.send_message(message.from_user.id, 'Кайф',
                           reply_markup=kb_admin if sqlite_db.is_admin(message.from_user.id) else kb_user)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.message_handler(start_make_form, commands=['Создать_профиль'], state=None)
    dp.message_handler(cancel_handler, commands='Отмена', state="*")
    dp.message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.message_handler(load_photo, state=FSMMakeForm.photo, content_types=['photo'])
    dp.message_handler(load_name, state=FSMMakeForm.name)
    dp.message_handler(load_description, state=FSMMakeForm.description)
    dp.message_handler(load_hashtags, state=FSMMakeForm.hashtags)
