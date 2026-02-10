# src/main.py - webhook + базовый обработчик
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web
from src.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! 👋\nЯ бот мониторинга талонов в Ижевске.\nВыбери регион /start")

async def on_startup():
    await bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
    print(f"Webhook установлен на {WEBHOOK_URL + WEBHOOK_PATH}")

async def main():
    await on_startup()
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, lambda request: dp.feed_webhook_update(bot, await request.json()))
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Webhook сервер запущен на порту {port}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
