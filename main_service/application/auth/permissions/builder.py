from application.auth.enums import PermissionsEnum
from application.auth.permissions.provider import PermissionProvider


class PermissionBuilder:
    def __init__(self):
        self.permissions = set()
        self.necessary = set()

    def providers(self, *providers: PermissionProvider) -> "PermissionBuilder":
        for provider in providers:
            self.permissions |= provider()
        return self

    def add(self, *args: PermissionsEnum) -> "PermissionBuilder":
        self.necessary |= args
        return self

    def apply(self):
        if not self.necessary <= self.permissions:
            raise PermissionError("Permission denied")
