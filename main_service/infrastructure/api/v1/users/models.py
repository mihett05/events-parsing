from datetime import datetime

from infrastructure.api.models import CamelModel


class UserModel(CamelModel):
    id: int
    email: str

    fullname: str
    is_active: bool

    telegram_id: int | None
    created_at: datetime
