from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_edit_profile = ReplyKeyboardMarkup(resize_keyboard=True).row('photo', 'name', 'description')
kb_edit_profile.add(KeyboardButton('hashtags')).insert(KeyboardButton('/cancеl'))
kb_cancel_edit = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancеl'))
