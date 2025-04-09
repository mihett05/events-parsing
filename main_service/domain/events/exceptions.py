from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExists, EntityNotFound


class EventNotFound(EntityNotFound):
    def __init__(self):
        super().__init__(Event)


class EventAlreadyExists(EntityAlreadyExists):
    def __init__(self):
        super().__init__(Event)
