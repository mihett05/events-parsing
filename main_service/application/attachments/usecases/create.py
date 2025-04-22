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
        self.repository = repository

    async def __call__(
        self, dto: CreateAttachmentDto, actor: User | None
    ) -> Attachment:
        async with self.__transaction as transaction:
            attachment = await self.repository.create(dto)
            try:
                return await self.gateway.create(attachment)
            except Exception:
                await transaction.rollback()
                raise
