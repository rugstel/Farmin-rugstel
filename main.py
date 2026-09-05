import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импортируем модули database и config
import database
import config

# Инициализация бота
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

class MiningStates(StatesGroup):
    mining = State()

# Функция для создания клавиатуры с кнопкой "Копать"
def get_mining_keyboard(income: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"⛏ Копать (+{income})",
        callback_data="mine"
    )
    return builder.as_markup()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    # Регистрируем пользователя в базе, если его нет
    database.register_user(user_id, username)
    
    # Получаем данные пользователя
    user_data = database.get_user(user_id)
    income = user_data.get('income', 1)
    
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n"
        f"Добро пожаловать в шахту! ⛏\n\n"
        f"Твоя руда: {user_data.get('ore', 0)}\n"
        f"Доход за клик: {income}"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_mining_keyboard(income)
    )

# Обработчик нажатия на кнопку "Копать"
@dp.callback_query(F.data == "mine")
async def mine_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    # Проверяем, зарегистрирован ли пользователь
    if not database.user_exists(user_id):
        await callback.answer("Сначала используй /start", show_alert=True)
        return
    
    # Получаем данные пользователя
    user_data = database.get_user(user_id)
    last_click = user_data.get('last_click')
    ore = user_data.get('ore', 0)
    income = user_data.get('income', 1)
    
    # Проверяем, прошло ли 5 секунд
    if last_click:
        last_click_time = datetime.fromisoformat(last_click)
        time_diff = datetime.now() - last_click_time
        if time_diff.total_seconds() < 5:
            wait_seconds = 5 - int(time_diff.total_seconds())
            await callback.answer(f"⏳ Подожди {wait_seconds} сек!", show_alert=True)
            return
    
    # Добавляем руду
    new_ore = ore + income
    database.update_user(user_id, {
        'ore': new_ore,
        'last_click': datetime.now().isoformat()
    })
    
    # Обновляем кнопку с новым значением дохода
    await callback.message.edit_reply_markup(
        reply_markup=get_mining_keyboard(income)
    )
    
    await callback.answer(f"⛏ Добыто +{income} руды!", show_alert=False)

# Обработчик команды /status
@dp.message(Command("status"))
async def status_command(message: Message):
    user_id = message.from_user.id
    
    if not database.user_exists(user_id):
        await message.answer("Сначала используй /start для регистрации")
        return
    
    user_data = database.get_user(user_id)
    
    # Формируем текст статуса
    status_text = (
        f"📊 <b>Твой статус</b>\n\n"
        f"💎 <b>Руда:</b> {user_data.get('ore', 0)}\n"
        f"⛏ <b>Шахты:</b> {user_data.get('mines', 0)}\n"
        f"🏭 <b>Фабрики:</b> {user_data.get('factories', 0)}\n"
        f"💰 <b>Доход за клик:</b> {user_data.get('income', 1)}"
    )
    
    await message.answer(status_text, parse_mode="HTML")

# Главная функция запуска
async def main():
    # Инициализация базы данных
    database.init_db()
    
    # Запуск бота
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())