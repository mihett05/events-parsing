import application.events.permissions.strategies as strategies
from application.auth.permissions import PermissionProvider
from domain.events.entities import Event
from domain.users.entities import User


class EventPermissionProvider(PermissionProvider):
    def __init__(self, event: Event, actor: User):
        self.strategy = self.__get_strategy(event, actor)

    @staticmethod
    def __get_strategy(entity: Event, actor: User):
        if entity.owner_id == actor.id:
            return strategies.OwnerPermissionStrategy()
        if actor.id in entity.admins:
            return strategies.AdminPermissionStrategy()
        if actor.id in entity.members:
            return strategies.MemberPermissionStrategy()
        if entity.is_visible:
            return strategies.PublicPermissionStrategy()

    def __call__(self):
        return self.strategy and self.strategy.permissions or set()
