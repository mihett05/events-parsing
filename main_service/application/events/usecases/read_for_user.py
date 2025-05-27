from domain.events.dtos import ReadUserEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadUserEventsUseCase:
    """Кейс для получения событий пользователя.

    Обеспечивает загрузку списка событий, связанных с конкретным пользователем,
    с возможностью фильтрации и сортировки согласно заданным параметрам.
    """

    def __init__(self, repository: EventsRepository):
        """Инициализирует кейс использования с репозиторием событий."""

        self.__repository = repository

    async def __call__(self, dto: ReadUserEventsDto) -> list[Event]:
        """Выполняет чтение событий пользователя.

        Возвращает список событий, отфильтрованных по критериям,
        указанным в параметрах запроса (dto).
        """

        return await self.__repository.read_for_user(dto)
