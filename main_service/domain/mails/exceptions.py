from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExists, EntityNotFound, EntityException


class MailNotFound(EntityNotFound):
    def __init__(self):
        super().__init__(Event)


class MailAlreadyExists(EntityAlreadyExists):
    def __init__(self):
        super().__init__(Event)


class FailedParseMailError(Exception):

    def __init__(self):
        super().__init__(Event)
