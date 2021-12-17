from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(KeyboardButton('/profile')).insert(KeyboardButton('/help'))
kb_admin.add(KeyboardButton('/companion')).insert(KeyboardButton('/allsee'))
