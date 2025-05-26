from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider


class OrganizationPermissionProvider(PermissionProvider):
    __perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.SUPER_USER: {
            PermissionsEnum.CAN_DELETE_ORGANIZATION,
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
        },
        RoleEnum.SUPER_OWNER: {
            PermissionsEnum.CAN_DELETE_ORGANIZATION,
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
        },
        RoleEnum.SUPER_ADMIN: {
            PermissionsEnum.CAN_UPDATE_ORGANIZATION,
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
        user_role: UserOrganizationRole,
        organization_id: int,
    ):
        self.permissions = self.__get_perms(user_role, organization_id)

    def __get_perms(
        self,
        user_role: UserOrganizationRole,
        organization_id: int,
    ) -> set[PermissionsEnum]:
        result = self.__perms.get(RoleEnum.PUBLIC).copy()
        if (
            user_role.role.value.startswith("SUPER")
            or user_role.organization_id == organization_id
        ):
            result |= self.__perms.get(user_role.role)
        return result

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions


class OrganizationLinkPermissionProvider(PermissionProvider):
    __max: set[PermissionsEnum] = {
        PermissionsEnum.CAN_CREATE_ORGANIZATION_LINK,
        PermissionsEnum.CAN_READ_ORGANIZATION_LINK,
        PermissionsEnum.CAN_DELETE_ORGANIZATION_LINK,
    }

    __perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.SUPER_USER: __max,
        RoleEnum.SUPER_OWNER: __max,
        RoleEnum.SUPER_ADMIN: __max,
        RoleEnum.SUPER_REDACTOR: set(),
        RoleEnum.OWNER: set(),
        RoleEnum.ADMIN: set(),
        RoleEnum.REDACTOR: set(),
        RoleEnum.PUBLIC: set(),
    }

    def __init__(self, user_role: UserOrganizationRole, organization_id: int = 0):
        self.permissions = self.__get_perms(user_role, organization_id)

    def __get_perms(
        self, user_role: UserOrganizationRole, organization_id: int
    ) -> set[PermissionsEnum]:
        result = self.__perms.get(RoleEnum.PUBLIC).copy()
        if (
            user_role.role.value.startswith("SUPER")
            or user_role.organization_id == organization_id
        ):
            result |= self.__perms.get(user_role.role)
        return result

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
