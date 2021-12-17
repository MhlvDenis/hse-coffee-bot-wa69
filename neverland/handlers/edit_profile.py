from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import kb_edit_profile, kb_cancel_edit, kb_user, kb_admin
from database import sqlite_db


class FSMMakeForm(StatesGroup):
    field = State()
    photo = State()
    content = State()


@dp.message_handler(commands=['edit'], state=None)
async def start_edit_form(message: types.Message):
    await FSMMakeForm.field.set()
    ret = await sqlite_db.sql_get_profile(message.from_user.id)
    await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nHashtags: {ret[3]}')
    await bot.send_message(message.from_user.id, 'Выбери, что хочешь изменить', reply_markup=kb_edit_profile)


@dp.message_handler(state="*", commands=['cancеl'])
@dp.message_handler(Text(equals='cancеl', ignore_case=True), state="*")
async def cancel_edit_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Ok',
                           reply_markup=kb_admin if sqlite_db.is_admin(message.from_user.id) else kb_user)


@dp.message_handler(state=FSMMakeForm.field)
async def load_field(message: types.Message, state: FSMContext):
    if message.text in ['photo', 'name', 'description', 'hashtags']:
        async with state.proxy() as data:
            data['field'] = message.text
            data['photo'] = ''
        await FSMMakeForm.next()
        if message.text != 'photo':
            await FSMMakeForm.next()
            if message.text == 'name':
                await message.reply('Введи новое имя')
            elif message.text == 'description':
                await message.reply('Придумай новое описание')
            else:
                await message.reply('Выбери себе новые хештеги')
        else:
            await message.reply('Выберу новую фотографию')
    else:
        await message.reply('Выбери из предложенных :)')


@dp.message_handler(content_types=['photo'], state=FSMMakeForm.photo)
async def load_photo_edit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['content'] = message.photo[0].file_id
        data['id'] = message.from_user.id
    await sqlite_db.set_field(state)
    await bot.send_message(message.from_user.id, 'Готово',
                           reply_markup=kb_admin if sqlite_db.is_admin(message.from_user.id) else kb_user)
    await state.finish()


@dp.message_handler(state=FSMMakeForm.content)
async def load_content(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['content'] = message.text
        data['id'] = message.from_user.id
    await sqlite_db.set_field(state)
    await bot.send_message(message.from_user.id, 'Готово',
                           reply_markup=kb_admin if sqlite_db.is_admin(message.from_user.id) else kb_user)
    await state.finish()


def register_handlers_edit_profile(dp: Dispatcher):
    dp.message_handler(start_edit_form, commands=['edit'], state=None)
    dp.message_handler(cancel_edit_handler, commands=['cancеl'], state="*")
    dp.message_handler(cancel_edit_handler, Text(equals='cancеl', ignore_case=True), state="*")
    dp.message_handler(load_photo_edit, state=FSMMakeForm.photo, content_types=['photo'])
    dp.message_handler(load_content, state=FSMMakeForm.content)
