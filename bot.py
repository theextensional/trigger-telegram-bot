"""Telegram бот реагирующий на фразы-триггеры."""
from aiogram import executor

from create_bot import dp
from handlers import admin, client

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
