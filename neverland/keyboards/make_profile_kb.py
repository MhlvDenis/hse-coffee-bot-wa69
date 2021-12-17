from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_make_profile = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('/create'), KeyboardButton('/help'))
kb_cancel_profile = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))
