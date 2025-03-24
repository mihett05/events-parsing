from abc import ABC
from typing import Any

from application.auth.enums import PermissionsEnum


class PermissionProvider(ABC):
    def __call__(
        self,
        *args: Any,
    ) -> set[PermissionsEnum]: ...
