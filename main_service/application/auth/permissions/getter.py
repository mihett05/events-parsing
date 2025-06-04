from uuid import UUID

from domain.users.entities import User
from domain.users.repositories import UsersRepository
from domain.users.role_getter import RoleGetter

from application.attachments.permissions.attachment import AttachmentPermissionProvider
from application.attachments.usecases import ReadAttachmentUseCase
from application.auth.enums import PermissionsEnum
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.organizations.permissions import OrganizationPermissionProvider
from application.organizations.usecases import ReadOrganizationUseCase


class PermissionGetter:
    def __init__(
        self,
        role_getter: RoleGetter,
        users_repository: UsersRepository,
        organization_use_case: ReadOrganizationUseCase,
        event_use_case: ReadEventUseCase,
        attachment_use_case: ReadAttachmentUseCase,
    ):
        self.__role_getter = role_getter
        self.__users_repository = users_repository
        self.__organization_use_case = organization_use_case
        self.__event_use_case = event_use_case
        self.__attachment_use_case = attachment_use_case

    async def get_attachment_perms(
        self, attachment_id: UUID, actor: User
    ) -> set[PermissionsEnum]:
        super_user = await self.__users_repository.get_super_user()
        attachment = await self.__attachment_use_case(attachment_id, super_user)
        event = await self.__event_use_case(attachment.event_id, super_user)
        role = await self.__role_getter(actor, event.organization_id)
        return AttachmentPermissionProvider(event.organization_id, role, event)()

    async def get_event_perms(self, event_id: int, actor: User) -> set[PermissionsEnum]:
        super_user = await self.__users_repository.get_super_user()
        event = await self.__event_use_case(event_id, super_user)
        role = await self.__role_getter(actor, event.organization_id)
        return EventPermissionProvider(event.organization_id, role, event)()

    async def get_organization_perms(
        self, organization_id: int, actor: User
    ) -> set[PermissionsEnum]:
        await self.__organization_use_case(organization_id)
        role = await self.__role_getter(actor, organization_id)
        return OrganizationPermissionProvider(role, organization_id)()
