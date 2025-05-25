from abc import ABCMeta, abstractmethod
from uuid import UUID

from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment


class AttachmentsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: CreateAttachmentDto) -> Attachment: ...

    @abstractmethod
    async def create_many(
        self, create_dtos: list[CreateAttachmentDto]
    ) -> list[Attachment]: ...

    @abstractmethod
    async def read(self, attachment_id: UUID) -> Attachment: ...

    @abstractmethod
    async def delete(self, attachment: Attachment) -> Attachment: ...

    @abstractmethod
    async def update(self, attachment: Attachment) -> Attachment: ...
