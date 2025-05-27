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

    """
    Ошибка, которая возвращается, если event не найден
    """


class EventAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Event)

    """
    Ошибка, которая возвращается, если такой event уже существует
    """


class InvalidEventPeriodError(InvalidEntityPeriodError):
    def __init__(self):
        super().__init__(Event)

    """
    Ошибка, которая возвращается, если у event start_date > end_date
    """


class EventAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()

    """
    Ошибка, которая возвращается, если недостаточно прав для действия
    """


class EventUserNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(EventUser)

    """
    Ошибка, которая возвращается, если не найден user или event для таблицы связки EventUser
    """


class EventUserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(EventUser)

    """
    Ошибка, которая возвращается, если данная строка EventUser уже существует
    """


class EventUserAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()

    """
    Ошибка, которая возвращается, если недостаточно прав для действия
    """
