from domain.events.dtos import ReadAllEventsFeedDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadForFeedEventsUseCase:
    """Кейс для получения событий для ленты.

    Предоставляет функционал для чтения событий, предназначенных для отображения
    в ленте, с учетом заданных параметров фильтрации и пагинации.
    """

    def __init__(self, repository: EventsRepository):
        """Инициализирует кейс использования с репозиторием событий."""

        self.__repository = repository

    async def __call__(self, dto: ReadAllEventsFeedDto) -> list[Event]:
        """Выполняет чтение событий для ленты.

        Возвращает список событий, отфильтрованных и подготовленных
        для отображения в ленте согласно переданным параметрам (dto).
        """

        return await self.__repository.read_for_feed(dto)
