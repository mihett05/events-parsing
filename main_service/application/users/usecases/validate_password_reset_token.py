from uuid import UUID

from domain.users.entities import User
from domain.users.repositories import PasswordResetTokenRepository, UsersRepository

from application.auth.tokens.dtos import TokenPairDto
from application.auth.tokens.gateways import SecurityGateway
from application.auth.usecases import CreateTokenPairUseCase
from application.transactions import TransactionsGateway
from application.users.dtos import UpdateUserPasswordDto


class ValidatePasswordResetToken:
    def __init__(
        self,
        users_repository: UsersRepository,
        token_repository: PasswordResetTokenRepository,
        tx: TransactionsGateway,
        create_token_pair_use_case: CreateTokenPairUseCase,
        security_gateway: SecurityGateway,
    ):
        self.__users_repository = users_repository
        self.__token_repository = token_repository
        self.__transaction = tx
        self.__create_token_pair_use_case = create_token_pair_use_case
        self.__security_gateway = security_gateway

    async def __call__(
        self, token_uuid: UUID, dto: UpdateUserPasswordDto
    ) -> tuple[User, TokenPairDto]:
        async with self.__transaction:
            token = await self.__token_repository.read(token_uuid)
            await self.__token_repository.change_token_used_statement(token.id)
            password_dto = self.__security_gateway.create_hashed_password(dto.password)
            token.user.hashed_password = password_dto.hashed_password
            token.user.salt = password_dto.salt
            await self.__users_repository.update(token.user)
            return token.user, await self.__create_token_pair_use_case(token.user)
