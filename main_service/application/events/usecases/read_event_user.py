from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository


class ReadEventUserUseCase:
    """Кейс использования для получения информации о связи пользователя с событием.

    Предоставляет данные о конкретном участии пользователя в указанном событии.
    """

    def __init__(
        self,
        repository: EventUsersRepository,
    ):
        """Инициализирует кейс с репозиторием связей пользователей и событий."""

        self.__repository = repository

    async def __call__(self, event_id: int, user_id: int) -> EventUser:
        """Возвращает информацию об участии пользователя в событии."""

        return await self.__repository.read(event_id, user_id)
