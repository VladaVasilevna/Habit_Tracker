from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение при вводе команды /start."""
    await update.message.reply_text("Привет! Я буду напоминать тебе о твоих привычках.")


def setup_bot():
    """Настройки Telegram bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    return application
