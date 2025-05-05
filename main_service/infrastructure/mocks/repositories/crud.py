from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError

Id = TypeVar("Id")
Entity = TypeVar("Entity")


@dataclass
class MockRepositoryConfig(metaclass=ABCMeta):
    entity: type[Entity]
    not_found_exception: type[EntityNotFoundError] = EntityNotFoundError
    already_exists_exception: type[EntityAlreadyExistsError] = (
        EntityAlreadyExistsError
    )

    def extract_id(self, entity: Entity) -> Id:
        return entity.id


def _storage_factory():
    storage = dict()

    def _factory(entity_type: Type):
        if storage.get(entity_type) is None:
            storage[entity_type] = dict()
        return storage[entity_type]

    return _factory


get_storage = _storage_factory()


class MockRepository(Generic[Entity, Id]):
    storage: dict[Id, Entity]
    __config: MockRepositoryConfig

    def __init__(self, config: MockRepositoryConfig):
        self.storage = get_storage(type(config.entity))
        self.__config = config

    async def create(self, entity: Entity) -> Entity:
        entity_id = self.__config.extract_id(entity)
        if entity_id in self.storage:
            raise self.__config.already_exists_exception()
        self.storage[self.__config.extract_id(entity)] = entity
        return entity

    async def read(self, entity_id: Id) -> Entity:
        if entity_id not in self.storage:
            raise self.__config.not_found_exception()
        return self.storage[entity_id]

    async def read_all(self) -> list[Entity]:
        return list(self.storage.values())

    async def update(self, entity: Entity) -> Entity:
        entity_id = self.__config.extract_id(entity)
        if entity_id not in self.storage:
            raise self.__config.not_found_exception()
        self.storage[entity_id] = entity
        return entity

    async def delete(self, entity: Entity) -> Entity:
        entity_id = self.__config.extract_id(entity)
        if entity_id not in self.storage:
            raise self.__config.not_found_exception()
        self.storage.pop(entity_id)
        return entity

    async def clear(self):
        self.storage.clear()
