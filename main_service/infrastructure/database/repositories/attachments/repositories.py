from uuid import UUID

from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)
from domain.attachments.repositories import AttachmentsRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db
from .models import AttachmentDatabaseModel


class AttachmentsDatabaseRepository(AttachmentsRepository):
    """Репозиторий для работы с вложениями в базе данных."""

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория вложений."""

        def __init__(self):
            super().__init__(
                model=AttachmentDatabaseModel,
                entity=Attachment,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=map_create_dto_to_model,
                not_found_exception=AttachmentNotFoundError,
                already_exists_exception=AttachmentAlreadyExistsError,
            )

    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий с указанной асинхронной сессией."""

        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, dto: CreateAttachmentDto) -> Attachment:
        """Создает новое вложение на основе DTO."""

        return await self.__repository.create_from_dto(dto)

    async def create_many(
        self, create_dtos: list[CreateAttachmentDto]
    ) -> list[Attachment]:
        """Создает несколько вложений на основе списка DTO."""
        return await self.__repository.create_many_from_dto(create_dtos)

    async def read(self, attachment_id: UUID) -> Attachment:
        """Получает вложение по идентификатору."""

        return await self.__repository.read(attachment_id)

    async def delete(self, attachment: Attachment) -> Attachment:
        """Удаляет указанное вложение."""

        return await self.__repository.delete(attachment)

    async def update(self, attachment: Attachment) -> Attachment:
        """Обновляет данные вложения."""

        return await self.__repository.update(attachment)
