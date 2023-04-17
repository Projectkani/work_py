import aiogram
import logging
from dotenv import load_dotenv
from aiogram import types
from aiogram.types import ParseMode
import sqlite3
import time
import os
from datetime import timedelta
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Unauthorized

load_dotenv() #Создайте файл .env

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN')) #В файл .env запишите: TOKEN=токен от @botfather
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('work.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, name TEXT, work_count INTEGER, last_used INTEGER)''')
conn.commit()

# обработка текстовой команды
@dp.message_handler()
async def messages_hand(msg: types.Message):
    words = msg.text
    if words == 'Ворк':
        await work(msg)
    elif words == 'ворк':
        await work(msg)
    else:
        return
# обработка команды через / ! .
@dp.message_handler(commands=['work','работать'], commands_prefix='.!/')
async def work(message: types.Message):
    user_id = message.from_user.id
    now = int(time.time())
# смотрим последние использование
    cursor.execute('SELECT last_used FROM users WHERE id=?', (user_id,))
    last_used = cursor.fetchone()
# проверяем что оно было более 3 часов назад, если меньше, то выдаёт текст и отменяет команду.
    if last_used and now - last_used[0] < 10800:
        remaining_time = timedelta(seconds=(10800 - (now - last_used[0])))
        remaining_time_str = str(remaining_time).split('.')[0]
        await message.reply(f"До следующей смены ещё:<b> {remaining_time_str} </b>.\n"
                            f"Попей пока чаю, порешай сканворды, или посмотри аниме <b>@reker_anime_bot</b>",
                            parse_mode=ParseMode.HTML)
        return
# Добавляем человека, дату использования и смену
    cursor.execute('INSERT OR IGNORE INTO users (id, name, work_count, last_used) VALUES (?, ?, 0, ?)',
                   (user_id, message.from_user.full_name, now))
    cursor.execute('UPDATE users SET work_count=work_count+1, last_used=? WHERE id=?', (now, user_id)) #count+1 = кол-во смен добавляемых в бд.
    conn.commit()
# Просматриваем кол-во смен
    cursor.execute('SELECT work_count FROM users WHERE id=?', (user_id,))
    work_count = cursor.fetchone()[0]
# отправляем текст
    await message.reply(f"Ты отработал: {work_count} смен!")

# Обработка топа. показывает первых 10рых.
@dp.message_handler(commands=['top_work'], commands_prefix='.!/')
async def work_stats(message: types.Message):
    cursor.execute('SELECT name, work_count FROM users ORDER BY work_count DESC LIMIT 10')
    rows = cursor.fetchall()

    text = "Список самых отбитых работяг мира:\n"
    for i, row in enumerate(rows):
        text += "{}. {}: {} смен\n".format(i + 1, row[0], row[1])
    await message.reply(text)

executor.start_polling(dp, skip_updates=True)