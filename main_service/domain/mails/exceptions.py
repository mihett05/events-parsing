from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class MailNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Event)


class MailAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Event)
