# src/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # загружает .env (Railway использует Variables, но dotenv тоже работает)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Webhook настройки (Railway сам подставит домен)
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN', 'localhost')}{WEBHOOK_PATH}"

# Для теста выводим в лог
print("BOT_TOKEN:", BOT_TOKEN[:10] + "..." if BOT_TOKEN else "NOT_SET")
print("DATABASE_URL:", "set" if DATABASE_URL else "NOT_SET")
print("WEBHOOK_URL:", WEBHOOK_URL)
