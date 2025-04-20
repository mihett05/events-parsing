from application.auth.tokens.dtos import TokenPairDto
from application.auth.tokens.gateways import TokensGateway
from domain.users.entities import User


class CreateTokenPairUseCase:
    def __init__(self, tokens_gateway: TokensGateway):
        self.tokens_gateway = tokens_gateway

    async def __call__(self, user: User) -> TokenPairDto:
        return await self.tokens_gateway.create_token_pair(user.email)
