from domain.events.entities import Event
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider


class EventPermissionProvider(PermissionProvider):
    __admin_perms: set[PermissionsEnum] = {
        PermissionsEnum.CAN_DELETE_EVENT,
        PermissionsEnum.CAN_READ_EVENT,
        PermissionsEnum.CAN_UPDATE_EVENT,
    }
    __member_perms: set[PermissionsEnum] = {
        PermissionsEnum.CAN_READ_EVENT,
    }
    __public_perms: set[PermissionsEnum] = {
        PermissionsEnum.CAN_READ_EVENT,
    }

    def __init__(self, event: Event, actor: User | None):
        self.permissions = self.__get_perms(event, actor)

    def __get_perms(self, entity: Event, actor: User | None) -> set[PermissionsEnum]:
        # P.S. for this moment it should be a plug
        # Because Event entyty does not complete
        return self.__admin_perms

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
