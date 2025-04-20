from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class EventNotFoundErrorError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Event)


class EventAlreadyExistsErrorError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Event)
