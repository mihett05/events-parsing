from domain.exceptions import (
    EntityAlreadyExists,
    EntityNotFound,
)
from domain.mails.entities import Mail


class MailNotFound(EntityNotFound):
    def __init__(self):
        super().__init__(Mail)


class MailAlreadyExists(EntityAlreadyExists):
    def __init__(self):
        super().__init__(Mail)


class FailedFetchMailError(Exception):
    def __init__(self):
        super().__init__("Failed to fetch mail from inbox")


class FailedParseMailError(Exception):
    def __init__(self):
        super().__init__("Failed to parse mail from inbox")
