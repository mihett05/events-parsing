from uuid import UUID

from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.attachments.gateways import FilesGateway
from application.attachments.permissions.attachment import (
    AttachmentPermissionProvider,
)
from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway


class DeleteAttachmentUseCase:
    def __init__(
        self,
        gateway: FilesGateway,
        tx: TransactionsGateway,
        repository: AttachmentsRepository,
        builder: PermissionBuilder,
        role_getter: RoleGetter,
        read_event_use_case: ReadEventUseCase,
    ):
        self.__gateway = gateway
        self.__transaction = tx
        self.__repository = repository
        self.__builder = builder
        self.__role_getter = role_getter
        self.__read_event_use_case = read_event_use_case

    async def __call__(self, attachment_id: UUID, actor: User) -> Attachment:
        async with self.__transaction:
            attachment = await self.__repository.read(attachment_id)
            event = None
            if attachment.event_id is not None:
                event = await self.__read_event_use_case(attachment.event_id, actor)
            organization_id = event and event.organization_id or -1
            actor_role = await self.__role_getter(actor, organization_id)
            self.__builder.providers(
                AttachmentPermissionProvider(organization_id, actor_role)
            ).add(
                PermissionsEnum.CAN_DELETE_ATTACHMENT,
            ).apply()

            attachment = await self.__repository.delete(attachment)

            return await self.__gateway.delete(attachment)
