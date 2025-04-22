from domain.attachments.entities import Attachment
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class AttachmentNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Attachment)


class AttachmentAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Attachment)
