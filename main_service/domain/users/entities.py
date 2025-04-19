from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str

    fullname: str
    is_active: bool = True

    salt: str = None
    hashed_password: str = None

    telegram_id: int | None = None
    created_at: datetime = None
