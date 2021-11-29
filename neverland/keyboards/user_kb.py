from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_user.add(KeyboardButton('/Мой_профиль')).insert(KeyboardButton('/help')).add(KeyboardButton('/Найти_сокофейника'))
