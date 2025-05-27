from domain.attachments.entities import Attachment
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class AttachmentNotFoundError(EntityNotFoundError):
    def __init__(self, path: str | None = None):
        super().__init__(Attachment, path=path)

    """
    Ошибка, которая возвращается, если аттачмент не найден
    """


class AttachmentAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Attachment)

    """
    Ошибка, которая возвращается, если такой аттачмент уже есть
    """
