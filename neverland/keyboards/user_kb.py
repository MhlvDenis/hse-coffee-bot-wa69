from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_user.add(KeyboardButton('/profile')).insert(KeyboardButton('/help')).add(KeyboardButton('/companion'))

kb_edit = ReplyKeyboardMarkup(resize_keyboard=True)
kb_edit.add(KeyboardButton('/photo')).insert(KeyboardButton('/name')).insert(KeyboardButton('/description'))
kb_edit.add(KeyboardButton('/hashtags')).insert(KeyboardButton('/cancel'))
