from domain.attachments.entities import Attachment
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class AttachmentNotFoundError(EntityNotFoundError):
    def __init__(self, path: str | None = None):
        super().__init__(Attachment, path=path)


class AttachmentAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Attachment)
