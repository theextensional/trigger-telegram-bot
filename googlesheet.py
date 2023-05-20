import os
import re
from typing import Any, List, Literal

from loguru import logger
from pygsheets import authorize
from pygsheets.client import Client
from pygsheets.spreadsheet import Spreadsheet
from pygsheets.worksheet import Worksheet

from models.trigger import Trigger

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class GoogleSheet:
    _client: Client
    _sh: Spreadsheet
    _wks: Worksheet
    _count_rows: int

    def _googlesheet_client(self, credential_file: str) -> Client:
        """It is authorized using the service key and returns the Google Docs
        client object"""
        logger.debug(credential_file)
        return authorize(service_file=credential_file)

    def _open_by_key(self) -> Spreadsheet:
        return self._client.open_by_key(self.googlesheet_file_key)

    def __init__(self, credential_file: str = "./credentials.json", googlesheet_file_key: str = "") -> None:
        """
        Initialize the class.

        Args:
            credential_file: The path to the credential file.
            googlesheet_file_key: The key of the Google Sheet file.
        """
        self.credential_file = credential_file
        self.googlesheet_file_key = googlesheet_file_key
        self._client = self._googlesheet_client(self.credential_file)
        self._sh = self._open_by_key()
        self._wks: Worksheet = self._sh.sheet1

    def match_cell(self, message: str) -> dict[Any, Any] | None:
        """
        This is a multi-line Google style docstring.

        Args:
            message (str): The message to be matched.

        Returns:
            dict[Any, Any] | None: The matched row or None.
        """
        logger.debug(f"`{message}`")
        if records := self._wks.get_all_records():
            self._count_rows = len(records)
            for row_id, row in enumerate(records, start=2):
                row["id"] = row_id
                if match := self.row_condtion(row, message):
                    logger.debug(match)
                    return match

    def row_condtion(self, row: dict[Any, Any], message: str) -> dict[Any, Any] | None:
        """
        Check if the message matches the trigger.

        Args:
            self: The class instance.
            row: The row from the database.
            message: The message to check.
            message_lower: The lowercase version of the message.

        Returns:
            The row if the message matches the trigger, otherwise None.
        """
        if row["regex"] == "TRUE" and re.search(row["trigger"], message, re.IGNORECASE):
            logger.debug("regex")
            return row
        if row["ignoreCase"] == "TRUE":
            row["trigger"] = row["trigger"].lower()
            message = message.lower()
        if (row["includes"] == "FALSE" and row["trigger"] == message) or (
            row["includes"] == "TRUE" and row["trigger"] in message
        ):
            return row

    def trigger_exists(self, value: str, col: int = 1) -> bool:
        return value in self._wks.get_col(col, include_tailing_empty=False)

    def add_trigger(self, trigger: Trigger) -> None:
        row = list(trigger.__dict__.values())
        logger.debug(row)
        self._wks.append_table(row)

    def set_count(self, trigger) -> Literal[False] | None:
        column_idx = len(trigger) - 1
        col_letter = chr(ord("@") + column_idx)
        counter = trigger["count"] + 1
        cell_address = f'{col_letter}{trigger["id"]}'
        logger.debug(f"{cell_address} = {counter}")
        return self._wks.update_value(cell_address, counter)

    def get_trigger(self, trigger_id: int) -> Trigger:
        row = self._wks.get_row(trigger_id)
        return Trigger(**row)

    def get_triggers(self) -> List[Trigger]:
        rows = self._wks.get_all_values()
        return [Trigger(**row) for row in rows]


if __name__ == "__main__":
    from environs import Env

    env = Env()
    env.read_env()
    g = GoogleSheet(
        env.str("CREDENTIAL_FILE"),
        env.str("GOOGLESHEET_FILE_KEY"),
    )
    match = g.match_cell("наш канал")
    logger.debug(match)
