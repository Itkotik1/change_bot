import asyncio
from aiogram import Bot, Dispatcher
from handlers.registration import registration_router
from handlers.bonuses_handler import bonuses_handler
from handlers.start_router import start_router
from handlers.admin_handlers import admin_handlers
from handlers.user_handlers import user_router
from data_base.database import init_db
import config


dp = Dispatcher()

async def main():
    await init_db()
    bot = Bot(token=config.BOT_TOKEN)
    dp.include_router(start_router)
    dp.include_router(bonuses_handler)
    dp.include_router(registration_router)
    dp.include_router(admin_handlers)
    dp.include_router(user_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')