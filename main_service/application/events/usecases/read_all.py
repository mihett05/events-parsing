from domain.events.dtos import ReadAllEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadAllEventUseCase:
    """Кейс использования для получения списка событий.

    Обеспечивает чтение списка событий с возможностью фильтрации и пагинации.
    """

    def __init__(self, repository: EventsRepository):
        """Инициализирует кейс с репозиторием событий."""

        self.__repository = repository

    async def __call__(self, dto: ReadAllEventsDto) -> list[Event]:
        """Возвращает список событий, соответствующих критериям фильтрации.

        Параметры выборки задаются через DTO объект, включая пагинацию и фильтры.
        """

        return await self.__repository.read_all(dto)
