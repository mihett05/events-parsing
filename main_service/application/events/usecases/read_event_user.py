from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository


class ReadEventUserUseCase:
    def __init__(
        self,
        repository: EventUsersRepository,
    ):
        self.__repository = repository

    async def __call__(self, event_id: int, user_id: int) -> EventUser:
        return await self.__repository.read(event_id, user_id)
