from domain.events.dtos import ReadAllEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadAllEventUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadAllEventsDto) -> list[Event]:
        if (
            dto.start_date is not None
            and dto.end_date is not None
            or dto.page is not None
            and dto.page_size is not None
        ):
            return await self.__repository.read_all(dto)
        raise ValueError("Invalid form dto readalleventsdto")
