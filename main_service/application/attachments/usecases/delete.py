from uuid import UUID

from application.attachments.gateways import FilesGateway
from application.transactions import TransactionsGateway
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User


class DeleteAttachmentUseCase:
    def __init__(
        self,
        gateway: FilesGateway,
        tx: TransactionsGateway,
        repository: AttachmentsRepository,
    ):
        self.__gateway = gateway
        self.__transaction = tx
        self.__repository = repository

    async def __call__(
        self, attachment_id: UUID, actor: User | None
    ) -> Attachment:
        async with self.__transaction:
            attachment = await self.__repository.read(attachment_id)
            attachment = await self.__repository.delete(attachment)

            return await self.__gateway.delete(attachment)
