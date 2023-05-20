import json
import sys
from typing import Any

from aiogram import Dispatcher, types
from loguru import logger

from create_bot import bot


def log_error(
    e: Exception,
    trigger: dict[str, Any],
    message: str,
) -> None:
    """
    Logs the error to the logger.

    Args:
        e: The exception that was raised.
        trigger: The trigger that caused the exception.
        message: The message that was being processed when the exception was
            raised.
    """
    if tb := sys.exc_info()[2]:
        filename = tb.tb_frame.f_code.co_filename
        line_number = tb.tb_lineno
        logger.error(
            f"{type(e).__name__}: {e}"
            f"\nModule: {type(e).__module__}"
            f"\nFile: {filename}:{line_number}"
            f"\nTrigger: {trigger}\nMessage: {message}"
        )


def caption(text: str) -> str:
    """
    This function cuts the text to the length of the caption.

    Args:
        text (str): Text to be cut.
        logger (logging.Logger): Logger for logging.

    Returns:
        str: Cut text.
    """
    if not text:
        return text
    logger.debug(f"Caption_input: {len(text)}")
    CAPTION_LENGTH = 1036
    if len(text) > CAPTION_LENGTH:
        OVERFLOW_TEXT = "... *Часть текста отсутствует!*"
        logger.debug(f"Caption_output: {len(text)}")
        text = text[: (CAPTION_LENGTH - len(OVERFLOW_TEXT))] + OVERFLOW_TEXT
    return text


async def send_welcome(message: types.Message) -> None:
    """Обработчик команд `/start` и `/help`.

    Args:
        message (types.Message): объект сообщения
    """
    await message.reply("Hi!\nI'm triggerBot!")


async def trigger(message: types.Message) -> None:
    """Триггер.
    Реагирует на сообщения, совпадающие с данными из гугл-таблицы.

    Args:
        message (types.Message): объект сообщения
    """
    if not (trigger := bot.googlesheet.match_cell(message.text)):
        return
    answer = ""
    if "content" in trigger and trigger["content"]:
        answer += trigger["content"].replace("**", "*").replace("> ", "")
        answer += "\n\n"
    if "embed" in trigger and trigger["embed"]:
        logger.debug(f"Embed: {trigger['embed']}")
        embed = json.loads(trigger["embed"])
        if "author" in embed:
            author = embed["author"]
            answer += author["name"] + "\n" if "url" not in author else f"[{author['name']}]({author['url']})\n\n"
        if "title" in embed:
            if "url" in embed:
                answer += f"[{embed['title']}]({embed['url']})\n\n"
            else:
                answer += f"*{embed['title']}*\n\n"
        if "description" in embed:
            answer += embed["description"].replace("*", "\\*") + "\n\n"
        if "image" in embed:
            image = embed["image"]["url"]
            extension = image.split(".")[-1].lower()
            answer = caption(answer)
            if extension in ["jpg", "jpeg", "png"]:
                try:
                    await message.reply_photo(
                        image,
                        caption=answer,
                        parse_mode=types.ParseMode.MARKDOWN,
                    )
                    bot.googlesheet.set_count(trigger)
                except Exception as e:
                    log_error(e, trigger, message.text)
                return
            try:
                await message.reply_document(
                    image,
                    caption=answer,
                    parse_mode=types.ParseMode.MARKDOWN,
                )
                bot.googlesheet.set_count(trigger)
            except Exception as e:
                log_error(e, trigger, message.text)
            return
        if "fields" in embed:
            for field in embed["fields"]:
                if "name" in field:
                    answer += f"*{field['name']}*\n"
                if "value" in field:
                    answer += field["value"].replace("*", "\\*") + "\n"

    if "attachments" in trigger and trigger["attachments"]:
        logger.debug("Attachments: {}", trigger["attachments"])
        for attachment in trigger["attachments"].split("\n"):
            extension = attachment.split(".")[-1].lower()
            answer = caption(answer)
            if extension in ["jpg", "jpeg"]:
                try:
                    await message.reply_photo(
                        attachment,
                        caption=answer,
                        parse_mode=types.ParseMode.MARKDOWN,
                    )
                except Exception as e:
                    log_error(e, trigger, message.text)
                    return
                continue
            try:
                await message.reply_document(
                    attachment,
                    caption=answer,
                    parse_mode=types.ParseMode.MARKDOWN,
                )
            except Exception as e:
                log_error(e, trigger, message.text)
                return

        bot.googlesheet.set_count(trigger)
        return

    logger.debug("Answer: {}", answer.strip())
    await message.reply(
        answer.replace("_", "\\_"),
        parse_mode=types.ParseMode.MARKDOWN,
    )
    bot.googlesheet.set_count(trigger)


def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(send_welcome, commands=["start", "help"])
    dp.register_message_handler(trigger)
