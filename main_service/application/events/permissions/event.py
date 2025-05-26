from domain.events.entities import Event
from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider


class EventPermissionProvider(PermissionProvider):
    __maximum_perms = {
        PermissionsEnum.CAN_CREATE_EVENT,
        PermissionsEnum.CAN_DELETE_EVENT,
        PermissionsEnum.CAN_READ_EVENT,
        PermissionsEnum.CAN_UPDATE_EVENT,
    }

    __public_event_permissions = {PermissionsEnum.CAN_READ_EVENT}

    __perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.SUPER_USER: __maximum_perms,
        RoleEnum.SUPER_OWNER: __maximum_perms,
        RoleEnum.SUPER_ADMIN: __maximum_perms,
        RoleEnum.SUPER_REDACTOR: __maximum_perms,
        RoleEnum.OWNER: __maximum_perms,
        RoleEnum.ADMIN: __maximum_perms,
        RoleEnum.REDACTOR: __maximum_perms,
        RoleEnum.PUBLIC: set(),
    }

    def __init__(
        self,
        organization_id: int,
        user_role: UserOrganizationRole,
        event: Event | None = None,
    ):
        self.permissions = self.__get_perms(organization_id, user_role, event)

    def __get_perms(
        self,
        organization_id: int,
        user_role: UserOrganizationRole,
        event: Event | None = None,
    ) -> set[PermissionsEnum]:
        result = self.__perms.get(RoleEnum.PUBLIC).copy()
        if event and event.is_visible:
            result |= self.__public_event_permissions
        if (
            user_role.role.value.startswith("SUPER")
            or user_role.organization_id == organization_id
        ):
            result |= self.__perms.get(user_role.role)
        return result

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
