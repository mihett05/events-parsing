from domain.exceptions import (
    EntityAlreadyExistsError,
    EntityException,
    EntityNotFoundError,
)
from domain.mails.entities import Mail


class MailNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Mail)


class MailAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Mail)


class FailedFetchMailError(EntityException):
    def __init__(self):
        super().__init__("Failed to fetch mail from inbox")


class FailedCreateMailError(EntityException):
    def __init__(self):
        super().__init__("Failed to create mail")


class FailedParseMailError(EntityException):
    def __init__(self):
        super().__init__("Failed to parse mail from inbox")
