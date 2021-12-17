from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_user.add(KeyboardButton('/edit')).insert(KeyboardButton('/help')).add(KeyboardButton('/companion'))
