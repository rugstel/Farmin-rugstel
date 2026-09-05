import sqlite3
from datetime import datetime

DB_NAME = "mining_bot.db"

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            ore INTEGER DEFAULT 0,
            mines INTEGER DEFAULT 0,
            factories INTEGER DEFAULT 0,
            income INTEGER DEFAULT 1,
            last_click TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def register_user(user_id: int, username: str):
    """Регистрация нового пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, ore, mines, factories, income)
        VALUES (?, ?, 0, 0, 0, 1)
    ''', (user_id, username))
    
    conn.commit()
    conn.close()

def user_exists(user_id: int) -> bool:
    """Проверка существования пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

def get_user(user_id: int) -> dict:
    """Получение данных пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, username, ore, mines, factories, income, last_click
        FROM users WHERE user_id = ?
    ''', (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'user_id': row[0],
            'username': row[1],
            'ore': row[2],
            'mines': row[3],
            'factories': row[4],
            'income': row[5],
            'last_click': row[6]
        }
    return None

def update_user(user_id: int, data: dict):
    """Обновление данных пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    update_fields = []
    values = []
    
    for key, value in data.items():
        update_fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(user_id)
    
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()