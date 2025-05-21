from domain.users.entities import User
from domain.users.repositories import UsersRepository

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.dtos import UpdateUserDto
from application.users.permissions import UserPermissionProvider
from application.users.usecases import ReadUserRolesUseCase, ReadUserUseCase


class UpdateUserUseCase:
    def __init__(
        self,
        repository: UsersRepository,
        read_user_use_case: ReadUserUseCase,
        tx: TransactionsGateway,
        permission_builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__repository = repository
        self.__read_roles_use_case = read_roles_use_case
        self.__builder = permission_builder
        self.__read_user_use_case = read_user_use_case
        self.__transaction = tx

    async def __call__(self, dto: UpdateUserDto, actor: User | None) -> User:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                UserPermissionProvider(roles, dto.user_id, actor.id)
            ).add(PermissionsEnum.CAN_UPDATE_USER).apply()
            user = await self.__read_user_use_case(dto.user_id)
            user.fullname = dto.fullname
            if dto.telegram_id:
                user.telegram_id = dto.telegram_id
            return await self.__repository.update(user)
