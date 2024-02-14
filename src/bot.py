import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import bot_token, interval
from handlers import commands, user, callbacks, states, apsched
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)  # Обьект бота
dp = Dispatcher()  # Диспетчер
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(apsched.time_cheking, trigger='interval', seconds=interval, kwargs={'bot': bot})

dp.include_routers(commands.router,
                   callbacks.router,
                   states.router,
                   user.router)  # Подключение роутеров из отдельных файлов к корневому


async def main():
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускаем все предыдущие сообщения
    await dp.start_polling(bot)  # Запускаем прослушку

if __name__ == "__main__":
    asyncio.run(main())
