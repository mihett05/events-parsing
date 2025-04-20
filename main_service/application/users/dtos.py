from dataclasses import dataclass


@dataclass
class UpdateUserDto:
    user_id: int
    fullname: str
    telegram_id: int | None = None
