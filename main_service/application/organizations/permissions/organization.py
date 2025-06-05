from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum

from application.auth.enums import PermissionsEnum
from application.auth.permissions.provider import PermissionProvider


class OrganizationPermissionProvider(PermissionProvider):
    """
    Провайдер разрешений для операций с организациями.

    Определяет набор доступных действий для каждой роли пользователя
    в контексте работы с организацией.
    """

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
        """
        Инициализация провайдера разрешений для организации.
        """

        self.permissions = self.__get_perms(user_role, organization_id)

    def __get_perms(
        self,
        user_role: UserOrganizationRole,
        organization_id: int,
    ) -> set[PermissionsEnum]:
        """
        Определяет набор разрешений на основе роли пользователя.
        """

        result = self.__perms.get(RoleEnum.PUBLIC).copy()
        if (
            user_role.role.value.startswith("SUPER")
            or user_role.organization_id == organization_id
        ):
            result |= self.__perms.get(user_role.role)
        return result

    def __call__(self) -> set[PermissionsEnum]:
        """
        Возвращает набор разрешений для текущего пользователя.
        """

        return self.permissions


class OrganizationLinkPermissionProvider(PermissionProvider):
    """
    Провайдер разрешений для работы со связями организаций.

    Определяет права доступа для операций создания, чтения и удаления
    связей между организациями.
    """

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
        """
        Инициализация провайдера разрешений для связей организаций.
        """

        self.permissions = self.__get_perms(user_role, organization_id)

    def __get_perms(
        self, user_role: UserOrganizationRole, organization_id: int
    ) -> set[PermissionsEnum]:
        """
        Определяет набор разрешений для работы со связями организаций.
        """

        result = self.__perms.get(RoleEnum.PUBLIC).copy()
        if (
            user_role.role.value.startswith("SUPER")
            or user_role.organization_id == organization_id
        ):
            result |= self.__perms.get(user_role.role)
        return result

    def __call__(self) -> set[PermissionsEnum]:
        """
        Возвращает набор разрешений для текущего пользователя.
        """

        return self.permissions
