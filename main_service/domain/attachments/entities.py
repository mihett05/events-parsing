from dataclasses import dataclass

from domain.attachments.enums import (
    AttachmentContentTypeEnum,
    AttachmentStorageTypeEnum,
)


@dataclass
class Attachment:
    owner_id: int

    path: str
    type: AttachmentStorageTypeEnum

    content: bytes
    content_type: AttachmentContentTypeEnum
