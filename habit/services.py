import requests
from config.settings import BOT_TOKEN, TELEGRAM_URL


def send_tg_message(text, chat_id):
    """Функция отправки сообщения в телеграм"""
    params = {
        "text": text,
        "chat_id": chat_id,
    }
    requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", params=params)
