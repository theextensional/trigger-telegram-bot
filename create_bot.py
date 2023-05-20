import sys

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from environs import Env
from loguru import logger

from googlesheet import GoogleSheet

env = Env()
env.read_env()

logger.remove()
logger.add(sys.stderr, level=env.int("LOG_LEVEL"))


class TelegramBot(Bot):
    def __init__(
        self,
        token,
        googlesheet: GoogleSheet | None = None,
    ) -> None:
        super().__init__(
            token,
        )
        if googlesheet:
            self.googlesheet: GoogleSheet = googlesheet


bot: TelegramBot = TelegramBot(
    token=env.str("BOT_TOKEN"),
    googlesheet=GoogleSheet(
        env.str("CREDENTIAL_FILE"),
        env.str("GOOGLESHEET_FILE_KEY"),
    ),
)
dp = Dispatcher(bot)

logger.add(
    env.str("ERROR_LOG_FILE"),
    format="{time} {level} {message}",
    level="WARNING",
    rotation="10 MB",
    compression="tar.xz",
)
logger.add(
    env.str("INFO_LOG_FILE"),
    format="{time} {level} {message}",
    level="INFO",
    rotation="10 MB",
    compression="tar.xz",
)
logger.debug("✅ Бот запущен")
