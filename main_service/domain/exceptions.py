from typing import TypeVar

Entity = TypeVar("Entity")


class EntityException(Exception):
    pass


class EntityNotFound(EntityException):
    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"{entity.__name__} not found")


class EntityAlreadyExists(EntityException):
    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"{entity.__name__} already exists")
