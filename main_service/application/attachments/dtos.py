from dataclasses import dataclass

from domain.attachments.enums import AttachmentContentTypeEnum


@dataclass
class CreateAttachmentDto:
    file_name: str
    content: bytes
    content_type: AttachmentContentTypeEnum
