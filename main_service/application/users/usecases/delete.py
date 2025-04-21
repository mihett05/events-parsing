from application.transactions import TransactionsGateway
from domain.users.entities import User
from domain.users.repositories import UsersRepository

from .read import ReadUserUseCase


class DeleteUserUseCase:
    def __init__(
        self,
        repository: UsersRepository,
        read_user_use_case: ReadUserUseCase,
        tx: TransactionsGateway,
    ):
        self.__repository = repository
        self.__read_user_use_case = read_user_use_case
        self.__transaction = tx

    async def __call__(self, actor: User) -> User:
        async with self.__transaction:
            user = await self.__read_user_use_case(actor.id)
            return await self.__repository.delete(user)
