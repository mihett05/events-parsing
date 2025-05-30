from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)
from domain.attachments.repositories import AttachmentsRepository
from domain.exceptions import EntityAccessDenied
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.attachments.gateways import FilesGateway
from application.attachments.permissions.attachment import (
    AttachmentPermissionProvider,
)
from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway


class CreateAttachmentUseCase:
    """UseCase для создания вложений.

    Обеспечивает процесс создания вложений, включая проверку прав доступа,
    транзакционное выполнение операций и обработку ошибок.
    """

    def __init__(
        self,
        gateway: FilesGateway,
        tx: TransactionsGateway,
        repository: AttachmentsRepository,
        builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        """Инициализирует зависимости UseCase."""

        self.__gateway = gateway
        self.__transaction = tx
        self.__repository = repository
        self.__builder = builder
        self.__role_getter = role_getter

    async def __try_create_attachment(
        self, dto: CreateAttachmentDto
    ) -> Attachment | None:
        """Пытается создать вложение в транзакционном контексте.

        В случае ошибок при создании файла откатывает транзакцию.
        Возвращает созданное вложение при успехе или None при ошибке.
        """

        async with self.__transaction.nested() as nested:
            attachment = await self.__repository.create(dto)
            try:
                await self.__gateway.create(attachment, dto.content)
            except AttachmentNotFoundError:
                print("exception1")
                await nested.rollback()
            except AttachmentAlreadyExistsError:
                print("exception2")
                await nested.rollback()
            else:
                print("commit")
                await nested.commit()
                return attachment

    def __has_perms(self, organization_id, roles):
        """Проверяет наличие прав на создание вложения в организации."""

        try:
            self.__builder.providers(
                AttachmentPermissionProvider(organization_id, roles)
            ).add(
                PermissionsEnum.CAN_CREATE_ATTACHMENT,
            ).apply()
            return True
        except EntityAccessDenied:
            return False

    async def __call__(
        self, dtos: list[CreateAttachmentDto], actor: User
    ) -> tuple[list[Attachment], list[str]]:
        """Выполняет создание нескольких вложений.

        Возвращает кортеж из списка успешно созданных вложений
        и списка имен файлов, которые не удалось создать.
        """

        failed = []
        succeed = []
        async with self.__transaction:
            for dto in dtos:
                actor_role = await self.__role_getter(actor, dto.event.organization_id)
                if self.__has_perms(
                    dto.event and dto.event.organization_id or -1, actor_role
                ) and (attachment := await self.__try_create_attachment(dto)):
                    succeed.append(attachment)
                else:
                    failed.append(f"{dto.filename}{dto.extension}")
        return succeed, failed
