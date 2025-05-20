import traceback
from abc import ABCMeta
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from sqlalchemy import Delete, Insert, Select, Update, insert, select
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
        return self._add_where_id(select(self.model), model_id)

    def get_default_select_all_query(self, ids: list[Id]) -> Select:
        return (
            select(self.model)
            .where(self.model.id.in_(ids))
            .order_by(self.model.id)
        )

    def get_select_all_query(self, _: Any) -> Select:
        return select(self.model).order_by(self.model.id)

    def _add_where_id(
        self, statement: Select | Update | Delete, model_id: Id
    ) -> Select | Update | Delete:
        return statement.where(self.model.id == model_id)

    def extract_id_from_entity(self, entity: Entity) -> Id:
        return entity.id

    def extract_id_from_model(self, model: ModelType) -> Id:
        return model.id

    def add_options(self, statement: Executable) -> Executable:
        return statement.options(*self.get_options())

    def get_options(self) -> list[LoaderOption]:
        return []


class PostgresRepository(metaclass=ABCMeta):
    config: PostgresRepositoryConfig

    def __init__(self, session: AsyncSession, config: PostgresRepositoryConfig):
        self.session = session
        self.config = config

    async def __create_models(self, models: list[ModelType]) -> list[Entity]:
        try:
            query = (
                insert(self.config.model)
                .values(list(map(self.__model_to_dict, models)))
                .returning(self.config.model)
            )
            return await self.get_entities_from_query(query)
        except IntegrityError:
            traceback.print_exc()
            raise self.config.already_exists_exception()

    async def create(self, model: ModelType) -> Entity:
        try:
            self.session.add(model)
            if self.__should_commit():
                await self.session.commit()
            await self.session.merge(model)
            return await self.read(self.config.extract_id_from_model(model))
        except IntegrityError:
            traceback.print_exc()
            raise self.config.already_exists_exception()

    async def get_scalar_or_none(self, query: Select) -> ModelType | None:
        return (
            await self.session.execute(self.config.add_options(query))
        ).scalar_one_or_none()

    async def get_entities_from_query(
        self, query: Select | Update | Insert
    ) -> list[Entity]:
        result = await self.session.scalars(self.config.add_options(query))
        return [
            self.config.entity_mapper(model) for model in result.unique().all()
        ]

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
        return await self.get_entities_from_query(
            self.config.get_default_select_all_query(model_ids)
        )

    async def create_from_dto(self, dto: CreateModelType) -> Entity:
        return await self.create(self.config.create_model_mapper(dto))

    async def create_from_entity(self, entity: Entity) -> Entity:
        return await self.create(self.config.model_mapper(entity))

    async def create_many_from_dto(
        self, dtos: list[CreateModelType]
    ) -> list[Entity]:
        models = [self.config.create_model_mapper(dto) for dto in dtos]
        return await self.__create_models(models)

    async def create_many_from_entity(
        self, dtos: list[CreateModelType]
    ) -> list[Entity]:
        models = [self.config.model_mapper(dto) for dto in dtos]
        return await self.__create_models(models)

    async def update(self, entity: Entity) -> Entity:
        await self.read(self.config.extract_id_from_entity(entity))

        model = self.config.model_mapper(entity)
        await self.session.merge(model)
        if self.__should_commit():
            await self.session.commit()
        return self.config.entity_mapper(model)

    async def delete(self, entity: Entity) -> Entity:
        if model := await self.session.get(
            self.config.model, self.config.extract_id_from_entity(entity)
        ):
            await self.session.delete(model)
            if self.__should_commit():
                await self.session.commit()
            return entity
        raise self.config.not_found_exception()

    @staticmethod
    def __should_commit() -> bool:
        return transaction_var.get() is None

    @staticmethod
    def __model_to_dict(model: ModelType) -> dict:
        return {
            column.key: getattr(model, column.key)
            for column in model.__table__.columns
            if getattr(model, column.key) is not None
        }
