from application.attachments.usecases import CreateAttachmentUseCase
from application.transactions import TransactionsGateway
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository
from domain.users.entities import User


class CreateMailsUseCase:
    def __init__(
        self,
        repository: MailsRepository,
        tx: TransactionsGateway,
        create_attachments_use_case: CreateAttachmentUseCase,
    ):
        self.__repository = repository
        self.__transaction = tx
        self.__create_attachments = create_attachments_use_case

    async def __call__(
        self, dtos: list[CreateMailDto], actor: User | None
    ) -> tuple[list[Mail], list[str]]:
        failed: list[str] = []
        succeed: list[Mail] = []

        async with self.__transaction:
            for dto in dtos:
                mail = await self.__try_create_mail(dto, actor)
                if mail is not None:
                    succeed.append(mail)
                else:
                    failed.append(dto.imap_mail_uid)
        return succeed, failed

    async def __try_create_mail(
        self, dto: CreateMailDto, actor: User | None
    ) -> Mail | None:
        async with self.__transaction.nested() as nested:
            mail = await self.__repository.create(dto)
            if len(dto.attachments) == 0:
                return mail

            succeed, _ = await self.__create_attachments(dto.attachments, actor)
            if len(succeed) > 0:
                await nested.commit()
                return mail

            await nested.rollback()
