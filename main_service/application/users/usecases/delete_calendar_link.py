from domain.users.entities import User
from domain.users.exceptions import CalendarUUIDNotFoundError
from domain.users.repositories import UsersRepository


class DeleteCalendarLinkUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, actor: User):
        if actor.settings.calendar_uuid is not None:
            actor.settings.calendar_uuid = None
            return await self.__repository.update(actor)
        raise CalendarUUIDNotFoundError
