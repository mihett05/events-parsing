import domain.notifications.dtos as dtos
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.exceptions import (
    NotificationAlreadyExistsError,
    NotificationNotFoundError,
)
from domain.notifications.repositories import NotificationsRepository
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db
from .models import NotificationDatabaseModel


class NotificationsDatabaseRepository(NotificationsRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=NotificationDatabaseModel,
                entity=Notification,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=map_create_dto_to_model,
                not_found_exception=NotificationNotFoundError,
                already_exists_exception=NotificationAlreadyExistsError,
            )

        def get_select_all_query(
            self, dto: dtos.ReadNotificationsDto
        ) -> Select:
            return (
                select(self.model)
                .where(self.model.status == NotificationStatusEnum.UNSENT)
                .order_by(self.model.id)
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__config = self.Config()
        self.__repository = PostgresRepository(session, self.__config)

    async def read(self, notification_id: int) -> Notification:
        return await self.__repository.read(notification_id)

    async def read_all(
        self, dto: dtos.ReadNotificationsDto
    ) -> list[Notification]:
        return await self.__repository.read_all(dto)

    async def create(self, dto: dtos.CreateNotificationDto) -> Notification:
        return await self.__repository.create_from_dto(dto)

    async def delete(self, notification: Notification) -> Notification:
        return await self.__repository.delete(notification)
