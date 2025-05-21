from domain.events.entities import Event, EventUser
from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidEntityPeriodError,
)


class EventNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Event)


class EventAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Event)


class InvalidEventPeriodError(InvalidEntityPeriodError):
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
