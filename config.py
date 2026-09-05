# config.py
# Файл конфигурации для бота

import os

# TODO: Замените "ВАШ_ТОКЕН" на реальный токен бота, полученный от @BotFather
BOT_TOKEN = "8257848684:AAGkZ_tllHKVE-IIHWsJerJqoAip4P4wexs"  # ← ВСТАВЬТЕ СВОЙ ТОКЕН

# Определяем окружение (для Vercel)
IS_VERCEL = os.getenv("VERCEL") == "1"
