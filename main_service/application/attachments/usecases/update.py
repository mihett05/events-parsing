from domain.attachments.dtos import UpdateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.users.entities import User

from application.attachments.gateways import FilesGateway
from application.attachments.permissions.attachment import (
    AttachmentPermissionProvider,
)
from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.usecases import ReadEventUseCase
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class UpdateAttachmentUseCase:
    def __init__(
        self,
        gateway: FilesGateway,
        repository: AttachmentsRepository,
        tx: TransactionsGateway,
        builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
        read_event_use_case: ReadEventUseCase,
    ):
        self.__gateway = gateway
        self.__repository = repository
        self.__transaction = tx
        self.__builder = builder
        self.__read_roles_use_case = read_roles_use_case
        self.__read_event_use_case = read_event_use_case

    async def __call__(
        self, attachment_update_dto: UpdateAttachmentDto, actor: User
    ) -> Attachment:
        async with self.__transaction:
            attachment = await self.__repository.read(
                attachment_update_dto.attachment_id
            )
            roles = await self.__read_roles_use_case(actor.id)
            event = None

            if attachment.event_id is not None:
                event = await self.__read_event_use_case(attachment.event_id, actor)

            self.__builder.providers(
                AttachmentPermissionProvider(
                    event and event.organization_id or -1,
                    roles,
                    event,
                )
            ).add(
                PermissionsEnum.CAN_UPDATE_ATTACHMENT,
            ).apply()

            attachment.filename = attachment_update_dto.filename
            return await self.__repository.update(attachment)
