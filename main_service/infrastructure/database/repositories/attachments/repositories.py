from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)
from domain.attachments.repositories import AttachmentsRepository

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db
from .models import AttachmentDatabaseModel


class AttachmentsDatabaseRepository(AttachmentsRepository):
    class Config(PostgresRepositoryConfig):
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
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, dto: CreateAttachmentDto) -> Attachment:
        return await self.__repository.create_from_dto(dto)

    async def read(self, attachment_id: UUID) -> Attachment:
        return await self.__repository.read(attachment_id)

    async def delete(self, attachment: Attachment) -> Attachment:
        return await self.__repository.delete(attachment)
