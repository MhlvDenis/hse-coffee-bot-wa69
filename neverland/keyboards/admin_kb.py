from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(KeyboardButton('/Мой_профиль')).insert(KeyboardButton('/help'))
kb_admin.add(KeyboardButton('/Найти_сокофейника')).insert(KeyboardButton('/Посмотреть_всех'))
