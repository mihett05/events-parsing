
from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError

from domain.mails.entities import Mail


class MailNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Mail)


class MailAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Mail)


class FailedFetchMailError(Exception):
    def __init__(self):
        super().__init__("Failed to fetch mail from inbox")


class FailedParseMailError(Exception):
    def __init__(self):
        super().__init__("Failed to parse mail from inbox")
