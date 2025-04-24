from datetime import datetime
from uuid import UUID

from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentNotFoundError,
    AttachmentAlreadyExistsError,
)
from domain.attachments.repositories import AttachmentsRepository
from domain.users import entities as entities
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError
from ..crud import Id, MockRepository, MockRepositoryConfig


class AttachmentsMemoryRepository(AttachmentsRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=User,
                not_found_exception=AttachmentNotFoundError,
                already_exists_exception=AttachmentAlreadyExistsError,
            )

        def extract_id(self, entity: User) -> Id:
            return entity.id

    def __init__(self):
        self.__repository = MockRepository(self.Config())

    async def read_by_email(self, email: str) -> entities.User:
        for user in await self.__repository.read_all():
            if user.email == email:
                return user
        raise UserNotFoundError()

    async def create(self, dto: CreateAttachmentDto) -> Attachment:
        attachment = Attachment(
            id=dto.id,
            filename=dto.filename,
            extension=dto.extension,
            mail_id=dto.mail and dto.mail.id,
            event_id=dto.event and dto.event.id,
            created_at=datetime.now(),
        )

        return await self.__repository.create(attachment)

    async def create_many(
        self, create_dtos: list[CreateAttachmentDto]
    ) -> list[Attachment]:
        return [await self.create(dto) for dto in create_dtos]

    async def read(self, attachment_id: UUID) -> Attachment:
        return await self.__repository.read(attachment_id)

    async def delete(self, attachment: Attachment) -> Attachment:
        return await self.__repository.delete(attachment)
