from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository
from domain.users.entities import User

from application.attachments.usecases import CreateAttachmentUseCase
from application.transactions import TransactionsGateway


class CreateMailUseCase:
    def __init__(
        self,
        repository: MailsRepository,
        tx: TransactionsGateway,
        create_attachments_use_case: CreateAttachmentUseCase,
    ):
        self.__repository = repository
        self.__transaction = tx
        self.__create_attachments_use_case = create_attachments_use_case

    async def __call__(
        self, dto: CreateMailDto, actor: User | None
    ) -> tuple[Mail, list[str]]:
        async with self.__transaction:
            mail = await self.__repository.create(dto)
            attachments, failed = await self.__create_attachments_use_case(
                dto.attachments, actor
            )
            mail.attachments = attachments
            return mail, failed
