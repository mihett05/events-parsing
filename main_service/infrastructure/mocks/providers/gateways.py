from aiogram import Bot
from application.attachments.gateways import FilesGateway
from application.auth.tokens.gateways import SecurityGateway, TokensGateway
from application.events.coordinator.gateway import CoordinatorGateway
from application.notifications.factory import NotificationGatewayAbstractFactory
from dishka import Provider, Scope, provide
from application.notifications.factory import NotificationGatewayAbstractFactory
from infrastructure.auth.bcrypt import BcryptSecurityGateway
from infrastructure.auth.jwt import JwtTokensGateway
from infrastructure.config import Config
from infrastructure.gateways.attachments import StaticDirFilesGateway
from infrastructure.gateways.notifications.factory import NotificationGatewayFactory
from infrastructure.gateways.notifications.gateways import (
    NotificationEmailGateway,
    NotificationTelegramGateway,
)
from infrastructure.mocks.gateways.events.gateway import (
    MemoryCoordinatorGateway,
)
from infrastructure.mocks.gateways.notifications.gateway import (
    NotificationEmailMemoryGateway,
)


class NotificationEmailMemoryGateway:
    pass


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    async def files_gateway(self, config: Config) -> FilesGateway:
        return StaticDirFilesGateway(base_path=config.static_folder)

    coordinator_publisher = provide(
        source=MemoryCoordinatorGateway, provides=CoordinatorGateway
    )
    notification_email_gateway = provide(
        source=NotificationEmailMemoryGateway, provides=NotificationEmailGateway
    )
    notification_gateway_factory = provide(
        source=NotificationGatewayFactory,
        provides=NotificationGatewayAbstractFactory,
    )
    telegram_notification_gateway = provide(NotificationTelegramGateway)

    @provide
    def telegram_bot(self, config: Config) -> Bot:
        return Bot(token=config.telegram_bot_token)

    tokens_gateway = provide(source=JwtTokensGateway, provides=TokensGateway)
    security_gateway = provide(source=BcryptSecurityGateway, provides=SecurityGateway)
    # TODO сделать гетевеи с заглушками
    notification_email_gateway = provide(
        source=NotificationEmailMemoryGateway, provides=NotificationEmailGateway
    )
    notification_gateway_factory = provide(
        source=NotificationGatewayFactory,
        provides=NotificationGatewayAbstractFactory,
    )
    telegram_notification_gateway = provide(NotificationTelegramGateway)

    @provide
    def telegram_bot(self, config: Config) -> Bot:
        return Bot(token=config.telegram_bot_token)
