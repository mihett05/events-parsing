from domain.events.dtos import CreateEventUserDto
from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository
from domain.users.entities import User


class CreateEventUserUseCase:
    """UseCase для создания связи пользователя с событием.

    Создает запись о принадлежности пользователя к событию.
    """

    def __init__(self, repository: EventUsersRepository):
        """Инициализирует репозиторий для работы с пользователями событий."""

        self.__repository = repository

    async def __call__(self, event_id: int, actor: User) -> EventUser:
        """Создает связь между пользователем и событием."""

        return await self.__repository.create(CreateEventUserDto(event_id, actor.id))
