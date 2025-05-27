from infrastructure.api.models import CamelModel


class UpdateAttachmentModelDto(CamelModel):
    """DTO для обновления данных вложения."""

    filename: str
