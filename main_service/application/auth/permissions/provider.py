from abc import ABCMeta

from application.auth.enums import PermissionsEnum


class PermissionProvider(metaclass=ABCMeta):
    def __call__(self) -> set[PermissionsEnum]: ...
