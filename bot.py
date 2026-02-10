import os
import logging
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
from telebot import types
import gspread
from google.oauth2.service_account import Credentials

# === НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_IDS = [int(x.strip()) for x in os.environ.get("CHAT_IDS", "").split(",") if x.strip()]
REMINDER_CHAT_IDS = [int(x.strip()) for x in os.environ.get("REMINDER_CHAT_IDS", "").split(",") if x.strip()]

# GOOGLE_CREDENTIALS из переменной окружения (будет добавлено на шаге 3)
import json
GOOGLE_CREDENTIALS = json.loads(os.environ.get("GOOGLE_CREDENTIALS_JSON"))

SHEET_URL = os.environ.get("SHEET_URL", "https://docs.google.com/spreadsheets/d/1pO7z5npjdIfwMa7z4fDIETs-JS21B5jnmkY1hO7NWuE/edit")
SHEET_TAB_NAME = os.environ.get("SHEET_TAB_NAME", "Дни рождения")

# === ОСТАЛЬНОЙ КОД БОТА (без изменений) ===
# ... вставьте сюда весь код из предыдущего сообщения (начиная с функции normalize_date) ...

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    
    if not TELEGRAM_TOKEN:
        logging.error("❌ Не задан TELEGRAM_TOKEN в переменных окружения!")
        exit(1)
    
    if not GOOGLE_CREDENTIALS:
        logging.error("❌ Не задан GOOGLE_CREDENTIALS_JSON в переменных окружения!")
        exit(1)
    
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    scheduler = BackgroundScheduler(timezone="Europe/Moscow")
    
    # ... остальной код инициализации бота ...
    
    # Запуск планировщика
    scheduler.add_job(send_reminder_notifications, 'cron', hour=17, minute=0)
    scheduler.add_job(send_today_notifications, 'cron', hour=9, minute=0)
    scheduler.add_job(send_today_notifications, 'cron', hour=12, minute=0)
    scheduler.start()
    
    logging.info("✅ Бот запущен и работает 24/7")
    logging.info(f"⏰ Напоминания: 17:00 МСК | Уведомления: 9:00 и 12:00 МСК")
    
    bot.polling(none_stop=True, interval=2, timeout=20)