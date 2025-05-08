from infrastructure.api.models import CamelModel


class UpdateAttachmentModelDto(CamelModel):
    filename: str
