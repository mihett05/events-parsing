from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository
from domain.users.entities import User

from application.attachments.usecases import CreateAttachmentUseCase
from application.transactions import TransactionsGateway


class CreateMailsUseCase:
    """
    Сценарий создания почтовых сообщений.

    Обеспечивает атомарное создание писем с вложениями,
    включая обработку ошибок и транзакционность операций.
    """

    def __init__(
        self,
        repository: MailsRepository,
        tx: TransactionsGateway,
        create_attachments_use_case: CreateAttachmentUseCase,
    ):
        """Инициализирует зависимости для создания писем."""

        self.__repository = repository
        self.__transaction = tx
        self.__create_attachments = create_attachments_use_case

    async def __call__(
        self, dtos: list[CreateMailDto], actor: User | None
    ) -> tuple[list[Mail], list[str]]:
        """
        Создает набор почтовых сообщений.

        Возвращает кортеж из списка успешно созданных писем
        и списка идентификаторов неудачных операций.
        """

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
        """
        Пытается создать письмо с вложениями в транзакции.

        В случае неудачи при создании вложений откатывает операцию.
        Возвращает созданное письмо или None при ошибке.
        """

        async with self.__transaction.nested() as nested:
            mail = await self.__repository.create(dto)
            if len(dto.attachments) == 0:
                return mail

            succeed, _ = await self.__create_attachments(dto.attachments, actor)
            if len(succeed) > 0:
                await nested.commit()
                return mail

            await nested.rollback()
