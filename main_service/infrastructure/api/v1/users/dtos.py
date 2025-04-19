from infrastructure.api.models import CamelModel


class UpdateUserModelDto(CamelModel):
    fullname: str
    telegram_id: int | None = None
