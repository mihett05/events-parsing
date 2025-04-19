from domain.events.entities import Event
from domain.exceptions import EntityAlreadyExists, EntityNotFound


class UserNotFound(EntityNotFound):
    def __init__(self):
        super().__init__(Event)


class UserAlreadyExists(EntityAlreadyExists):
    def __init__(self):
        super().__init__(Event)
