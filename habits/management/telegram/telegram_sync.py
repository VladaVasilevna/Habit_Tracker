import logging

import requests

from config.settings import BOT_TOKEN

logger = logging.getLogger(__name__)


def send_telegram_message_sync(chat_id, text):
    """Синхронная отправка сообщения через Telegram API"""
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
        response.raise_for_status()
        return True, "Сообщение отправлено"
    except requests.exceptions.RequestException as e:
        error_msg = f"Ошибка Telegram API: {str(e)}"
        if hasattr(e, "response") and e.response:
            error_msg += (
                f" (Status: {e.response.status_code}, Response: {e.response.text})"
            )
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Неожиданная ошибка: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
