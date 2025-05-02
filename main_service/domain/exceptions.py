from typing import TypeVar

Entity = TypeVar("Entity")


class EntityException(Exception):
    pass


class EntityNotFoundError(EntityException):
    def __init__(self, entity: type[Entity] | None = None, **kwargs):
        super().__init__(f"{entity.__name__} not found ({kwargs})")


class EntityAlreadyExistsError(EntityException):
    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"{entity.__name__} already exists")


class InvalidEntityPeriodError(EntityException):
    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"Invalid {entity.__name__} period")
