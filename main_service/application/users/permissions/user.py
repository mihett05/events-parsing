from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider


class UserPermissionProvider(PermissionProvider):
    __maximum_perms = {
        PermissionsEnum.CAN_READ_USER,
        PermissionsEnum.CAN_UPDATE_USER,
    }

    __perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.SUPER_USER: __maximum_perms,
        RoleEnum.SUPER_OWNER: __maximum_perms,
        RoleEnum.SUPER_ADMIN: __maximum_perms,
        RoleEnum.SUPER_REDACTOR: set(),
        RoleEnum.OWNER: set(),
        RoleEnum.ADMIN: set(),
        RoleEnum.REDACTOR: set(),
        RoleEnum.PUBLIC: set(),
    }

    def __init__(
        self,
        user_roles: list[UserOrganizationRole],
        user_id: int,
        actor_id: int,
    ):
        self.permissions = self.__get_perms(user_roles, user_id, actor_id)

    def __get_perms(
        self,
        user_roles: list[UserOrganizationRole],
        user_id: int,
        actor_id: int,
    ) -> set[PermissionsEnum]:
        result = self.__perms.get(RoleEnum.PUBLIC).copy()
        if user_id == actor_id:
            result |= self.__perms.get(RoleEnum.SUPER_USER)
        for role in user_roles:
            if role.role.value.startswith("SUPER"):
                result |= self.__perms.get(role.role)
        return result

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
