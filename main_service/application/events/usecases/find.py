from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class FindEventUseCase:
    """Кейс использования для поиска события."""

    def __init__(self, repository: EventsRepository):
        """Инициализирует кейс использования с указанным репозиторием."""

        self.__repository = repository

    async def __call__(self, dto: CreateEventDto) -> Event | None:
        """Выполняет поиск события на основе переданного DTO."""

        return await self.__repository.find(dto)
