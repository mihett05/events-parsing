from uuid import UUID

from application.attachments.gateways import FilesGateway
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User


class ReadAttachmentUseCase:
    def __init__(
        self, gateway: FilesGateway, repository: AttachmentsRepository
    ):
        self.__gateway = gateway
        self.__repository = repository

    async def __call__(
        self, attachment_id: UUID, actor: User | None
    ) -> Attachment:
        attachment = await self.__repository.read(attachment_id)
        return await self.__gateway.read(attachment)
