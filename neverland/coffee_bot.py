from aiogram.utils import executor
from create_bot import dp
from handlers import make_profile, admin, user
from database import sqlite_db


async def on_startup(_):
    print('start work')
    sqlite_db.sql_start()


user.register_handlers_user(dp)
admin.register_handlers_admin(dp)
make_profile.register_handlers_make_profile(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
