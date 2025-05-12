from domain.events.entities import Event, EventUser
from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)


class EventNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Event)


class EventAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Event)


class EventAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()


class EventUserNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(EventUser)


class EventUserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(EventUser)


class EventUserAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()
