from dataclasses import dataclass


@dataclass
class TelegramProfile:
    user_id: int
    telegram_id: int


@dataclass
class User:
    id: int
    email: str
    is_active: bool
    fullname: str
    salt: str
    hashed_password: str
    profile: TelegramProfile | None
