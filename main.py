# src/main.py
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from src.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def on_startup():
    await bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
    print(f"Webhook set to {WEBHOOK_URL + WEBHOOK_PATH}")

async def on_shutdown():
    await bot.delete_webhook()
    print("Webhook removed")

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
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    print(f"Webhook server started on port {os.getenv('PORT', 8080)}")
    await asyncio.Event().wait()  # Держим сервер живым

if __name__ == "__main__":
    asyncio.run(main())
