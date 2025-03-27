from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionProvider
from domain.events.entities import Event
from domain.users.entities import User


class EventPermissionProvider(PermissionProvider):
    __perms: dict[str, set[PermissionsEnum]] = {
        "Owner": {
            PermissionsEnum.CAN_READ_EVENT,
            PermissionsEnum.CAN_UPDATE_EVENT,
            PermissionsEnum.CAN_DELETE_EVENT,
        },
        "Admin": {
            PermissionsEnum.CAN_READ_EVENT,
            PermissionsEnum.CAN_UPDATE_EVENT,
        },
        "Member": {PermissionsEnum.CAN_READ_EVENT},
        "Public": {PermissionsEnum.CAN_READ_EVENT},
    }

    def __init__(self, event: Event, actor: User):
        self.permissions = self.__get_perms(event, actor) or set()

    def __get_perms(self, entity: Event, actor: User):
        if entity.owner_id == actor.id:
            return self.__perms["Public"]
        if actor.id in entity.admins:
            return self.__perms["Public"]
        if actor.id in entity.members:
            return self.__perms["Public"]
        if entity.is_visible:
            return self.__perms["Public"]

    def __call__(self):
        return self.permissions
