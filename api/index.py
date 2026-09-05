import sys
import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ========== ИНИЦИАЛИЗАЦИЯ ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== ВАШИ ХЕНДЛЕРЫ (КОПИРУЙТЕ ВАШ КОД) ==========
def get_mining_keyboard(income: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"⛏ Копать (+{income})", callback_data="mine")
    return builder.as_markup()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\nДобро пожаловать в шахту! ⛏\n\nТвоя руда: 0\nДоход за клик: 1",
        reply_markup=get_mining_keyboard(1)
    )

@dp.callback_query(lambda c: c.data == "mine")
async def mine_callback(callback: CallbackQuery):
    await callback.answer("⛏ Добыто +1 руды!", show_alert=False)

# ========== FASTAPI ==========
app = FastAPI()

@app.post("/api/bot")
async def webhook(request: Request):
    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.process_update(update)
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    webhook_url = "https://" + os.getenv("VERCEL_URL", "localhost") + "/api/bot"
    await bot.set_webhook(webhook_url)
    print(f"Webhook set to: {webhook_url}")
