import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import init_db
from handlers import router

async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()  # <- без аргументов
    dp.include_router(router)

    print("🚀 Бот запущен...")
    await dp.start_polling(bot)  # <- бот передается здесь

if __name__ == "__main__":
    asyncio.run(main())
