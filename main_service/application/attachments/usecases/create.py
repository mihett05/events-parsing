from typing import Iterable

from application.attachments.gateways import FilesGateway
from application.transactions import TransactionsGateway
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User


class CreateAttachmentUseCase:
    def __init__(
        self,
        gateway: FilesGateway,
        tx: TransactionsGateway,
        repository: AttachmentsRepository,
    ):
        self.gateway = gateway
        self.__transaction = tx
        self.__repository = repository

    async def __call__(
        self, dtos: list[CreateAttachmentDto], actor: User | None
    ) -> Iterable[Attachment]:
        collection = []
        async with self.__transaction as transaction:
            attachments = await self.__repository.create_many(dtos)
            for dto, attachment in zip(dtos, attachments):
                try:
                    collection.append(
                        await self.gateway.create(attachment, dto.content)
                    )
                except Exception:
                    await transaction.rollback()
                    raise
        return collection
