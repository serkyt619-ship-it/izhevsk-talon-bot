# src/main.py
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Я бот мониторинга талонов в Ижевске.\n"
        "Напиши /start для меню"
    )

async def on_startup():
    await bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
    print(f"Webhook установлен на {WEBHOOK_URL + WEBHOOK_PATH}")

async def on_shutdown():
    await bot.delete_webhook()
    print("Webhook удалён")

async def main():
    await on_startup()

    app = web.Application()
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    print(f"Webhook сервер запущен на порту {port}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
