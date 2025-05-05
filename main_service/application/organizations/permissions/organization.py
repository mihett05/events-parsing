from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider


class OrganizationPermissionProvider(PermissionProvider):
    __perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.SUPER_USER: {
            PermissionsEnum.CAN_DELETE_ORGANIZATION,
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
            PermissionsEnum.CAN_SEND_ORGANIZATION_LINK,
        },
        RoleEnum.SUPER_OWNER: {
            PermissionsEnum.CAN_DELETE_ORGANIZATION,
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
            PermissionsEnum.CAN_SEND_ORGANIZATION_LINK,
        },
        RoleEnum.SUPER_ADMIN: {
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
            PermissionsEnum.CAN_SEND_ORGANIZATION_LINK,
        },
        RoleEnum.SUPER_REDACTOR: set(),
        RoleEnum.OWNER: {
            PermissionsEnum.CAN_DELETE_ORGANIZATION,
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
        },
        RoleEnum.ADMIN: {
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
        },
        RoleEnum.REDACTOR: set(),
        RoleEnum.PUBLIC: set(),
    }

    def __init__(
        self,
        user_roles: list[UserOrganizationRole],
        organization_id: int = -1,
    ):
        self.permissions = self.__get_perms(user_roles, organization_id)

    def __get_perms(
        self,
        user_roles: list[UserOrganizationRole],
        organization_id: int = -1,
    ) -> set[PermissionsEnum]:
        result = self.__perms.get(RoleEnum.PUBLIC)
        for role in user_roles:
            if (
                role.role.value.startswith("SUPER")
                or role.organization_id == organization_id
            ):
                result |= self.__perms.get(role.role).copy()
        return result

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
