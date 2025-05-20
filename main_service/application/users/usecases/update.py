from domain.users.entities import User
from domain.users.repositories import UsersRepository

from application.transactions import TransactionsGateway
from application.users.dtos import UpdateUserDto
from application.users.usecases.read import ReadUserUseCase


class UpdateUserUseCase:
    def __init__(
        self,
        repository: UsersRepository,
        read_user_use_case: ReadUserUseCase,
        tx: TransactionsGateway,
    ):
        self.__repository = repository
        self.__read_user_use_case = read_user_use_case
        self.__transaction = tx

    async def __call__(self, dto: UpdateUserDto, actor: User) -> User:
        async with self.__transaction:
            user = await self.__read_user_use_case(dto.user_id)
            if dto.fullname:
                user.fullname = dto.fullname
            if dto.telegram_id:
                user.telegram_id = dto.telegram_id

            return await self.__repository.update(user)
