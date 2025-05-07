from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.notifications.permissions.notification import NotificationPermissionProvider
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase
from domain.notifications.dtos import CreateNotificationDto
from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository
from domain.users.entities import User


class CreateNotificationUseCase:
    def __init__(self, repository: NotificationsRepository, permission_builder: PermissionBuilder, transaction: TransactionsGateway, read_roles_use_case: ReadUserRolesUseCase
):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__read_roles_use_case = read_roles_use_case

    async def __call__(self, dto: CreateNotificationDto, actor: User | None) -> Notification:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                NotificationPermissionProvider(dto.organization_id, roles)
            ).add(PermissionsEnum.CAN_CREATE_EVENT).apply()
        return await self.__repository.create(dto)
