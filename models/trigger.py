from dataclasses import dataclass


@dataclass
class Trigger:
    trigger: str
    regex: bool = False
    ignoreCase: bool = True
    includes: bool = False
    content: str | None = None
    embed: str | None = None
    attachments: str | None = None
    note: str | None = None
    random: int | None = None
    count: int = 0
