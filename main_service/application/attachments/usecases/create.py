from typing import Iterable

from application.attachments.gateways import FilesGateway
from application.transactions import TransactionsGateway
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentNotFoundError,
    AttachmentAlreadyExistsError,
)
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User


class CreateAttachmentUseCase:
    def __init__(
        self,
        gateway: FilesGateway,
        tx: TransactionsGateway,
        repository: AttachmentsRepository,
    ):
        self.__gateway = gateway
        self.__transaction = tx
        self.__repository = repository

    async def __try_create_attachment(
        self, dto: CreateAttachmentDto
    ) -> Attachment | None:
        async with self.__transaction.nested() as nested:
            attachment = await self.__repository.create(dto)
            try:
                await self.__gateway.create(attachment, dto.content)
            except AttachmentNotFoundError:
                await nested.rollback()
            except AttachmentAlreadyExistsError:
                await nested.rollback()
            else:
                await nested.commit()
                return attachment

    async def __call__(
        self, dtos: list[CreateAttachmentDto], actor: User | None
    ) -> tuple[Iterable[Attachment], list[str]]:
        failed = []
        succeed = []
        async with self.__transaction:
            for dto in dtos:
                if attachment := await self.__try_create_attachment(dto):
                    succeed.append(attachment)
                else:
                    failed.append(f"{dto.filename}{dto.extension}")
        return succeed, failed
