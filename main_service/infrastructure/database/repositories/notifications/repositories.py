import domain.notifications.dtos as dtos
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.exceptions import (
    NotificationAlreadyExistsError,
    NotificationNotFoundError,
)
from domain.notifications.repositories import NotificationsRepository
from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db
from .models import NotificationDatabaseModel


class NotificationsDatabaseRepository(NotificationsRepository):
    """Репозиторий для работы с уведомлениями в базе данных.

    Обеспечивает основные CRUD операции для работы с уведомлениями,
    используя Postgres в качестве хранилища. Наследует базовую реализацию
    PostgresRepository, добавляя специфичную для уведомлений логику.
    """

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория уведомлений.

        Определяет маппинги между моделями и специфичные для домена
        исключения, а также настраивает базовые запросы.
        """

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

        def get_select_all_query(self, dto: dtos.ReadNotificationsDto) -> Select:
            """Формирует запрос для чтения списка уведомлений.

            Учитывает необходимость блокировки записей для обновления
            и фильтрует по статусу 'не отправлено'.
            """

            query = (
                select(self.model)
                .where(self.model.status == NotificationStatusEnum.UNSENT)
                .order_by(self.model.id)
            )
            if dto.for_update:
                query = query.with_for_update(skip_locked=True)

            return query

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__config = self.Config()
        self.__repository = PostgresRepository(session, self.__config)

    async def read(self, notification_id: int) -> Notification:
        """Получает уведомление по идентификатору."""
        return await self.__repository.read(notification_id)

    async def read_all(self, dto: dtos.ReadNotificationsDto) -> list[Notification]:
        """Возвращает список уведомлений согласно параметрам фильтрации."""
        return await self.__repository.read_all(dto)

    async def change_notifications_statuses(
        self, notifications: list[Notification], status: NotificationStatusEnum
    ):
        """Изменяет статус группы уведомлений на указанный."""

        ids = list(map(self.__config.extract_id_from_entity, notifications))
        query = (
            update(NotificationDatabaseModel)
            .where(NotificationDatabaseModel.id.in_(ids))
            .values(status=status)
            .execution_options(synchronize_session="fetch")
            .returning(self.__config.model)
        )
        await self.__session.execute(query)

    async def create(self, dto: dtos.CreateNotificationDto) -> Notification:
        """Создает новое уведомление на основе DTO."""

        return await self.__repository.create_from_dto(dto)

    async def create_many(self, entities: list[Notification]) -> list[Notification]:
        """Создает несколько уведомлений за одну операцию."""

        return await self.__repository.create_many_from_entity(entities)

    async def delete(self, notification: Notification) -> Notification:
        """Удаляет указанное уведомление."""

        return await self.__repository.delete(notification)
