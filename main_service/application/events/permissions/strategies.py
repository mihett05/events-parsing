from abc import ABC, abstractmethod

from application.auth.enums import PermissionsEnum


class PermissionStrategy(ABC):
    @abstractmethod
    def get_permissions(
        self,
    ) -> set[PermissionsEnum]: ...


class OwnerPermissionStrategy(PermissionStrategy):
    def get_permissions(self):
        return {
            PermissionsEnum.CAN_READ_EVENT,
            PermissionsEnum.CAN_UPDATE_EVENT,
            PermissionsEnum.CAN_DELETE_EVENT,
        }


class AdminPermissionStrategy(PermissionStrategy):
    def get_permissions(self):
        return {
            PermissionsEnum.CAN_READ_EVENT,
            PermissionsEnum.CAN_UPDATE_EVENT,
        }


class MemberPermissionStrategy(PermissionStrategy):
    def get_permissions(self):
        return {
            PermissionsEnum.CAN_READ_EVENT,
        }


class PublicPermissionStrategy(PermissionStrategy):
    def get_permissions(self):
        return {
            PermissionsEnum.CAN_READ_EVENT,
        }
