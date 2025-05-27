from typing import TypeVar

Entity = TypeVar("Entity")


class EntityException(Exception):
    pass
    """
    Стандартная ошибка от которой все ошибки наследуются
    """


class EntityNotFoundError(EntityException):
    def __init__(self, entity: type[Entity] | None = None, **kwargs):
        super().__init__(f"{entity.__name__} not found ({kwargs})")

    """
        Стандартная ошибка NotFound от которой все ошибки NotFound наследуются
    """


class EntityAlreadyExistsError(EntityException):
    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"{entity.__name__} already exists")

    """
        Стандартная ошибка AlreadyExists от которой все ошибки AlreadyExists наследуются
    """


class EntityAccessDenied(EntityException):
    def __init__(self):
        super().__init__("Access denied")

    """
        Стандартная ошибка AccessDenied от которой все ошибки AccessDenied наследуются
    """


class InvalidEntityPeriodError(EntityException):
    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"Invalid {entity.__name__} period")

    """
        Стандартная ошибка InvalidEntityPeriodError от которой все ошибки InvalidEntityPeriodError наследуются
    """
