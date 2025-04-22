from abc import ABCMeta
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
<<<<<<< HEAD
from sqlalchemy import Delete, Insert, Select, Update, select
=======
from sqlalchemy import Delete, Select, Update, select
>>>>>>> 734238dad51cb720fbb31b35c5efe9ed046573b5
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import Executable

from infrastructure.database.transactions import transaction_var

Id = TypeVar("Id")
Entity = TypeVar("Entity")
ModelType = TypeVar("ModelType")
CreateModelType = TypeVar("CreateModelType")


@dataclass
class PostgresRepositoryConfig(Generic[ModelType, Entity, Id]):
    model: type[ModelType]
    entity: type[Entity]
    entity_mapper: Callable[[ModelType], Entity]
    model_mapper: Callable[[Entity], ModelType]
    create_model_mapper: Callable[[CreateModelType], ModelType]
    not_found_exception: type[EntityNotFoundError] = EntityNotFoundError
    already_exists_exception: type[EntityAlreadyExistsError] = (
        EntityAlreadyExistsError
    )

    def get_select_query(self, model_id: Id) -> Select:
        return self.add_where_id(select(self.model), model_id)

    def get_default_select_all_query(self, ids: list[Id]) -> Select:
        return (
            select(self.model)
            .order_by(self.model.id)
            .where(self.model.id.in_(ids))
        )

    def get_select_all_query(self, dto: Any) -> Select:
        return select(self.model).order_by(self.model.id)

    def add_where_entity(
        self, statement: Select | Update | Delete, entity: Entity
    ) -> Select | Update | Delete:
        return self.add_where_id(statement, self.extract_id_from_entity(entity))

    def add_where_id(
        self, statement: Select | Update | Delete, model_id: Id
    ) -> Select | Update | Delete:
        return statement.where(self.model.id == model_id)

    def extract_id_from_entity(self, entity: Entity) -> Id:
        return entity.id

    def extract_id_from_model(self, model: ModelType) -> Id:
        return model.id

    def extract_id_from_models(self, models: list[ModelType]) -> list[Id]:
        return [self.extract_id_from_model(model) for model in models]

    def add_options(self, statement: Executable) -> Executable:
        return statement.options(*self.get_options())

    def get_options(self) -> list[LoaderOption]:
        return []


class PostgresRepository(metaclass=ABCMeta):
    config: PostgresRepositoryConfig

    def __init__(self, session: AsyncSession, config: PostgresRepositoryConfig):
        self.session = session
        self.config = config

    async def get_models_from_query(self, query: Select) -> list[ModelType]:
        return list(
            (await self.session.scalars(self.config.add_options(query))).all()
        )

    async def get_entities_from_query(self, query: Select) -> list[Entity]:
        return [
            self.config.entity_mapper(model)
            for model in await self.get_models_from_query(query)
        ]

    async def get_scalar_or_none(self, query: Select) -> ModelType | None:
        return (
            await self.session.execute(self.config.add_options(query))
        ).scalar_one_or_none()

    async def read(self, model_id: Id) -> Entity:
        if model := await self.session.get(
            self.config.model,
            model_id,
            options=self.config.get_options(),
            populate_existing=True,
        ):
            return self.config.entity_mapper(model)
        raise self.config.not_found_exception()

    async def read_all(self, dto: Any = None) -> list[Entity]:
        return await self.get_entities_from_query(
            self.config.get_select_all_query(dto)
        )

    async def read_by_ids(self, model_ids: list[Id]) -> list[Entity]:
        query = self.config.get_default_select_all_query(model_ids)
        return await self.get_entities_from_query(query)

    async def __create(self, model: ModelType) -> Entity:
        try:
            self.session.add(model)
            if self._should_commit():
                await self.session.commit()
            await self.session.refresh(model)
            return await self.read(self.config.extract_id_from_model(model))
        except IntegrityError:
            raise self.config.already_exists_exception()

    async def create_many(self, dtos: list[CreateModelType]) -> list[Entity]:
        models = [self.config.create_model_mapper(dto) for dto in dtos]
        try:
            self.session.add_all(models)
            if self._should_commit():
                await self.session.commit()

            for model in models:
                await self.session.refresh(model)
            return await self.read_by_ids(
                self.config.extract_id_from_models(models)
            )
        except IntegrityError:
            raise self.config.already_exists_exception()

    async def create_from_dto(self, dto: CreateModelType) -> Entity:
        model = self.config.create_model_mapper(dto)
        return await self.__create(model)

    async def create_from_entity(self, entity: Entity) -> Entity:
        model = self.config.model_mapper(entity)
        return await self.__create(model)

    async def update(self, entity: Entity) -> Entity:
        try:
            await self.read(self.config.extract_id_from_entity(entity))
        except EntityNotFoundError:
            raise self.config.not_found_exception()

        model = self.config.model_mapper(entity)
        await self.session.merge(model)
        if self._should_commit():
            await self.session.commit()
        return self.config.entity_mapper(model)

    async def delete(self, entity: Entity) -> Entity:
        if model := await self.session.get(
            self.config.model, self.config.extract_id_from_entity(entity)
        ):
            await self.session.delete(model)
            if self._should_commit():
                await self.session.commit()
            return entity
        raise self.config.not_found_exception()

    @staticmethod
    def _should_commit() -> bool:
        session = transaction_var.get()
        return session is None
