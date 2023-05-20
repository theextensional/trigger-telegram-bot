import os

from aiogram import Dispatcher, types
from environs import Env
from loguru import logger
from pyimgur import Imgur

from create_bot import bot
from models.trigger import Trigger

env = Env()
env.read_env()

TRIGGER_KEY = "+"
REGEX_TRIGGER_KEY = "="

UPLOAD_LIMIT_GIF = 8_000_000


def current_key(string: str, *keys) -> str | None:
    return next((key for key in keys if string.startswith(key)), None)


# function upload to imgur
def upload_to_imgur(file_path: str) -> str:
    im = Imgur(env.str("IMGUR_API_ID"))
    uploaded_image = im.upload_image(file_path)
    logger.debug(f"Upload to Imgur {uploaded_image.link}")
    return uploaded_image.link


async def attachment_handler(message: types.Message):
    if not message.reply_to_message.photo and not message.reply_to_message.document:
        return None

    if message.reply_to_message.photo:
        destination = await message.reply_to_message.photo[-1].download()
        uploaded_image = upload_to_imgur(destination.name)
        os.remove(destination.name)

        return uploaded_image

    print(message.reply_to_message.document.mime_type)

    if message.reply_to_message.document:
        if all(
            {
                message.reply_to_message.document.mime_type in ("image/png"),
                message.reply_to_message.document.file_size <= UPLOAD_LIMIT_GIF,
            }
        ):
            logger.debug("Document type is PNG or GIF")
            destination = await message.reply_to_message.document.download()
            uploaded_image = upload_to_imgur(destination.name)
            os.remove(destination.name)

            return uploaded_image
        elif message.reply_to_message.document.mime_type == "video/mp4":
            print(message.reply_to_message.document)

    return None

    # send warning message


def check_trigger_key(message: types.Message) -> str | None:
    return current_key(message.text, TRIGGER_KEY, REGEX_TRIGGER_KEY) or None


async def add_regex(message: types.Message) -> None:
    """
    Add regex trigger to the Google Sheet

    :param message: Message object
    :return: None
    """
    logger.debug(f"Add regex_trigger `{message.text}` to the Google Sheet")
    cur_key = current_key(message.text, *REGEX_TRIGGER_KEY)
    trigger = message.text.lstrip(cur_key).strip()
    status = f"❌ Триггер `{trigger}` уже существует"
    if not bot.googlesheet.trigger_exists(trigger):
        attachments = await attachment_handler(message)
        content = message.reply_to_message.caption or message.reply_to_message.text
        tg = Trigger(
            trigger, note=f"Добавил {message.from_user.full_name}", attachments=attachments, content=content, regex=True
        )
        bot.googlesheet.add_trigger(tg)
        status = f"✅ Триггер `{trigger}` успешно добавлен"

    await message.reply(status, parse_mode="markdown")


async def add_trigger(message: types.Message) -> None:
    """
    Add trigger to the Google Sheet

    :param message:
    :return:
    """
    logger.debug(f"Add trigger `{message.text}` to the Google Sheet")
    cur_key = current_key(message.text, TRIGGER_KEY)
    trigger = message.text.lstrip(cur_key).strip()
    status = f"❌ Триггер `{trigger}` уже существует"
    if not bot.googlesheet.trigger_exists(trigger):
        attachments = await attachment_handler(message)
        content = message.reply_to_message.caption or message.reply_to_message.text
        tg = Trigger(trigger, note=f"Добавил {message.from_user.full_name}", attachments=attachments, content=content)
        bot.googlesheet.add_trigger(tg)
        status = f"✅ Триггер `{trigger}` успешно добавлен"

    await message.reply(status, parse_mode="markdown")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        add_regex,
        lambda msg: msg.reply_to_message and msg.text.startswith(REGEX_TRIGGER_KEY) and len(msg.text) > 1,
        is_chat_admin=True,
    )
    dp.register_message_handler(
        add_trigger,
        lambda msg: msg.reply_to_message and msg.text.startswith(TRIGGER_KEY) and len(msg.text) > 1,
        is_chat_admin=True,
    )
