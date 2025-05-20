from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)
from domain.attachments.repositories import AttachmentsRepository
from domain.exceptions import EntityAccessDenied
from domain.users.entities import User

from application.attachments.gateways import FilesGateway
from application.attachments.permissions.attachment import (
    AttachmentPermissionProvider,
)
from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class CreateAttachmentUseCase:
    def __init__(
        self,
        gateway: FilesGateway,
        tx: TransactionsGateway,
        repository: AttachmentsRepository,
        builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__gateway = gateway
        self.__transaction = tx
        self.__repository = repository
        self.__builder = builder
        self.__read_roles_use_case = read_roles_use_case

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

    def __has_perms(self, organization_id, roles):
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
        failed = []
        succeed = []
        roles = await self.__read_roles_use_case(actor.id)
        async with self.__transaction:
            for dto in dtos:
                print(self.__has_perms(
                    dto.event and dto.event.organization_id or -1, roles
                ))
                if self.__has_perms(
                    dto.event and dto.event.organization_id or -1, roles
                ) and (attachment := await self.__try_create_attachment(dto)):
                    succeed.append(attachment)
                else:
                    failed.append(f"{dto.filename}{dto.extension}")
        return succeed, failed
