from application.attachments.gateways import FilesGateway
from application.auth.tokens.gateways import SecurityGateway, TokensGateway
from application.events.coordinator.gateway import CoordinatorGateway
from dishka import Provider, Scope, provide

from infrastructure.auth.bcrypt import BcryptSecurityGateway
from infrastructure.auth.jwt import JwtTokensGateway
from infrastructure.config import Config
from infrastructure.gateways.attachments import StaticDirFilesGateway
from infrastructure.mocks.gateways.events.gateway import (
    MemoryCoordinatorGateway,
)


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    async def files_gateway(self, config: Config) -> FilesGateway:
        return StaticDirFilesGateway(base_path=config.static_folder)

    coordinator_publisher = provide(
        source=MemoryCoordinatorGateway, provides=CoordinatorGateway
    )
    tokens_gateway = provide(source=JwtTokensGateway, provides=TokensGateway)
    security_gateway = provide(source=BcryptSecurityGateway, provides=SecurityGateway)
