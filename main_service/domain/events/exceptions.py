from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class EventNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Event)


class EventAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Event)
