from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User

from application.attachments.gateways import FilesGateway
from application.transactions import TransactionsGateway


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
    ) -> tuple[list[Attachment], list[str]]:
        # TODO: Переработать на функционал на создание либо всех, либо не одного
        #  т.е. в случае хотя бы одной ошибки поднимаем ексепшн
        #  сложность заключается в откате сохранения контента аттачментов
        #  т.к. ошибка происходит если упал гетевей, а значит откатить в нем - проблема
        #  Возможно решение - добавление состояния аттачменту и задача, которая удаляет failed
        #  чтобы в FileStorage не было пустышек

        failed = []
        succeed = []
        async with self.__transaction:
            for dto in dtos:
                if attachment := await self.__try_create_attachment(dto):
                    succeed.append(attachment)
                else:
                    failed.append(f"{dto.filename}{dto.extension}")
        return succeed, failed
