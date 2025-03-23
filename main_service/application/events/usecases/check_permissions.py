from domain.events.entities import Event
from domain.users.entities import User


class CheckPermissionsUseCase:

    async def __call__(self, event: Event, user: User) -> bool:
        return True
