from abc import ABC

from application.auth.enums import PermissionsEnum


class PermissionStrategy(ABC):
    __perms: set[PermissionsEnum]

    @property
    def permissions(self) -> set[PermissionsEnum]:
        return self.__perms.copy()


class OwnerPermissionStrategy(PermissionStrategy):
    __perms = {
        PermissionsEnum.CAN_READ_EVENT,
        PermissionsEnum.CAN_UPDATE_EVENT,
        PermissionsEnum.CAN_DELETE_EVENT,
        PermissionsEnum.CAN_SET_OWNER,
    }


class AdminPermissionStrategy(PermissionStrategy):
    __perms = {
        PermissionsEnum.CAN_READ_EVENT,
        PermissionsEnum.CAN_UPDATE_EVENT,
    }


class MemberPermissionStrategy(PermissionStrategy):
    __perms = {
        PermissionsEnum.CAN_READ_EVENT,
    }


class PublicPermissionStrategy(PermissionStrategy):
    __perms = {
        PermissionsEnum.CAN_READ_EVENT,
    }
