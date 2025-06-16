import asyncio

from telegram import Bot

from config.settings import BOT_TOKEN


async def send_test_message():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=88646334, text="Тестовое сообщение")


asyncio.run(send_test_message())
