from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(KeyboardButton('/edit')).insert(KeyboardButton('/help')).insert(KeyboardButton('/companion'))
kb_admin.add(KeyboardButton('/allhashtags')).insert(KeyboardButton('/allsee'))
