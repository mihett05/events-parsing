from uuid import UUID

from application.auth.tokens.dtos import TokenPairDto
from application.auth.usecases import CreateTokenPairUseCase
from application.transactions import TransactionsGateway
from application.users.usecases.read import ReadUserUseCase
from application.users.usecases.update import UpdateUserUseCase
from domain.users.entities import User
from domain.users.repositories import UsersRepository, ActivationTokenRepository


class ValidateActivationTokenUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
        token_repository: ActivationTokenRepository,
        read_user_use_case: ReadUserUseCase,
        tx: TransactionsGateway,
        create_token_pair_use_case: CreateTokenPairUseCase,
        update_user_use_case: UpdateUserUseCase,
    ):
        self.__users_repository = users_repository
        self.__token_repository = token_repository
        self.__read_user_use_case = read_user_use_case
        self.__transaction = tx
        self.__create_token_pair_use_case = create_token_pair_use_case
        self.update_user_use_case = update_user_use_case

    async def __call__(self, token_uuid: UUID) -> tuple[User, TokenPairDto]:
        token = await self.__token_repository.read_activation_token(token_uuid)
        async with self.__transaction:
            token.user.is_active = True
            await self.__users_repository.update(token.user)
            return token.user, await self.__create_token_pair_use_case(token.user)
