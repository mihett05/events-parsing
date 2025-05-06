from domain.events.entities import Event
from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider


class AttachmentPermissionProvider(PermissionProvider):
    __maximum_perms = {
        PermissionsEnum.CAN_READ_ATTACHMENT,
        PermissionsEnum.CAN_CREATE_ATTACHMENT,
    }

    __public_event_permissions = {
        PermissionsEnum.CAN_READ_ATTACHMENT
    }

    __perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.SUPER_USER: __maximum_perms,
        RoleEnum.SUPER_OWNER: __maximum_perms,
        RoleEnum.SUPER_ADMIN: __maximum_perms,
        RoleEnum.SUPER_REDACTOR: __maximum_perms,
        RoleEnum.OWNER: __maximum_perms,
        RoleEnum.ADMIN: __maximum_perms,
        RoleEnum.REDACTOR: __maximum_perms,
        RoleEnum.PUBLIC: {},
    }

    def __init__(
        self, organization_id: int, user_roles: list[UserOrganizationRole], event: Event | None = None
    ):
        self.permissions = self.__get_perms(organization_id, user_roles, event)

    def __get_perms(
        self, organization_id: int, user_roles: list[UserOrganizationRole], event: Event | None = None
    ) -> set[PermissionsEnum]:
        result = self.__perms.get(RoleEnum.PUBLIC)
        if event is not None and event.is_visible:
            result |= self.__public_event_permissions
        for role in user_roles:
            if (
                    role.role.value.startswith("SUPER")
                    or role.organization_id == organization_id
            ):
                result |= self.__perms.get(role.role).copy()
        return result

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
