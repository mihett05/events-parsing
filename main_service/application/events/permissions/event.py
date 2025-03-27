from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider
from domain.events.entities import Event
from domain.users.entities import User


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

    def __init__(self, event: Event, actor: User):
        self.permissions = self.__get_perms(event, actor)

    def __get_perms(self, entity: Event, actor: User) -> set[PermissionsEnum]:
        if actor.id in entity.admins:
            return self.__admin_perms
        if actor.id in entity.members:
            return self.__member_perms
        if entity.is_visible:
            return self.__public_perms
        return set()

    def __call__(self) -> set[PermissionsEnum]:
        return self.permissions
