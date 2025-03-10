import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram import F, Router
from aiogram.client.default import DefaultBotProperties
from app.handlers import router
import app.database as db
from api import TOKEN

logging.basicConfig(level=logging.INFO)

db.init_db()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
dp.include_router(router)

async def main():
    print('Bot had started.')
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot switched off.')
