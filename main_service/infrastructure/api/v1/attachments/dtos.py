from infrastructure.api.models import CamelModel


class UpdateAttachmentModelDto(CamelModel):
    attachment_id: int
    filename: str
