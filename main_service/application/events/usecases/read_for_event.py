from domain.events.dtos import ReadEventUsersDto
from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository
from domain.users.entities import User


class ReadEventUsersUseCase:
    """Кейс для получения списка пользователей, связанных с событием.

    Обеспечивает чтение данных о пользователях, участвующих в определенном событии,
    в соответствии с правами доступа вызывающего.
    """

    def __init__(self, repository: EventUsersRepository):
        """Инициализирует кейс использования с репозиторием для работы с пользователями событий."""

        self.__repository = repository

    async def __call__(self, dto: ReadEventUsersDto, actor: User) -> list[EventUser]:
        """Выполняет чтение пользователей события."""

        return await self.__repository.read_for_event(dto)
