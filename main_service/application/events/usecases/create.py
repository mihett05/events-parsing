from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.transactions import TransactionsGateway


class CreateEventUseCase:
    """UseCase для создания события.

    Обеспечивает процесс создания события с проверкой прав доступа
    и транзакционным выполнением операции.
    """

    def __init__(
        self,
        repository: EventsRepository,
        role_getter: RoleGetter,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGateway,
    ):
        """Инициализирует зависимости UseCase."""

        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__role_getter = role_getter

    async def __call__(self, dto: CreateEventDto, actor: User) -> Event:
        """Создает новое событие.

        Проверяет права пользователя на создание события
        и сохраняет новое событие в репозитории.
        Возвращает созданный объект события.
        """

        async with self.__transaction:
            actor_role = await self.__role_getter(actor, dto.organization_id)
            self.__builder.providers(
                EventPermissionProvider(dto.organization_id, actor_role)
            ).add(PermissionsEnum.CAN_CREATE_EVENT).apply()
            return await self.__repository.create(dto)
