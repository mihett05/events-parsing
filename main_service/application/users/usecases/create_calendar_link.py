from uuid import uuid4

from domain.users.entities import User
from domain.users.repositories import UsersRepository


class CreateCalendarLinkUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, base_url: str, actor: User) -> str:
        if actor.settings.calendar_uuid is None:
            uuid = uuid4()
            actor.settings.calendar_uuid = uuid
            await self.__repository.update(actor)
        else:
            uuid = actor.settings.calendar_uuid
        return f"{base_url}/v1/events/subscribe/ical/{uuid}"
