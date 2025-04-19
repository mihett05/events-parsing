from dataclasses import dataclass


@dataclass
class UpdateUserDto:
    id: int
    fullname: str
    telegram_id: int | None = None
