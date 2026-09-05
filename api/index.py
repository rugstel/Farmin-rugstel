import sys
import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import types

# Добавляем корневую папку в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем ВСЁ из вашего main.py
from main import bot, dp
from database import init_db

app = FastAPI()

# Эндпоинт для вебхука
@app.post("/api/bot")
async def webhook(request: Request):
    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.process_update(update)
    return {"status": "ok"}

# При запуске ставим вебхук и инициализируем БД
@app.on_event("startup")
async def on_startup():
    init_db()
    webhook_url = "https://" + os.getenv("VERCEL_URL", "localhost") + "/api/bot"
    await bot.set_webhook(webhook_url)
    print(f"Webhook set to: {webhook_url}")
