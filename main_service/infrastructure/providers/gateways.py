import logging
from typing import AsyncIterable

from application.attachments.gateways import FilesGateway
from application.auth.tokens.gateways import SecurityGateway, TokensGateway
from application.events.coordinator.gateway import CoordinatorGateway
from application.events.usecases import DeduplicateEventUseCase
from application.mails.gateway import EmailsGateway
from application.notifications.factory import NotificationGatewayAbstractFactory
from dishka import Provider, Scope, provide
from faststream.broker.message import StreamMessage
from faststream.rabbit import RabbitBroker
from miniopy_async import Minio

from infrastructure.auth.bcrypt import BcryptSecurityGateway
from infrastructure.auth.jwt import JwtTokensGateway
from infrastructure.config import Config
from infrastructure.gateways.attachments.minio import MinioFilesGateway
from infrastructure.gateways.mails.gateway import ImapEmailsGateway
from infrastructure.gateways.notifications.factory import (
    NotificationGatewayFactory,
)
from infrastructure.gateways.notifications.gateways import (
    NotificationEmailGateway,
    NotificationTelegramGateway,
)
from infrastructure.rabbit.events import (
    RabbitMQCoordinatorGateway,
)


class GatewaysProvider(Provider):
    """Провайдер зависимостей для всех шлюзов приложения."""

    scope = Scope.APP

    @provide
    def broker(self, config: Config) -> RabbitBroker:
        """Предоставляет брокер RabbitMQ для работы с очередями сообщений."""
        return RabbitBroker(config.rabbitmq_url, log_level=logging.DEBUG)

    @provide
    def minio(self, config: Config) -> Minio:
        """Предоставляет клиент MinIO для работы с объектным хранилищем."""

        return Minio(
            endpoint=config.minio_url,
            access_key=config.minio_root_user,
            secret_key=config.minio_root_password,
            secure=False,
        )

    @provide
    async def emails_gateway(self, config: Config) -> AsyncIterable[EmailsGateway]:
        """Предоставляет шлюз для работы с входящими email через IMAP."""

        async with ImapEmailsGateway(
            imap_server=config.imap_server,
            imap_username=config.imap_username,
            imap_password=config.imap_password,
        ) as gateway:
            yield gateway

    @provide
    async def notification_email_gateway(
        self, config: Config
    ) -> AsyncIterable[NotificationEmailGateway]:
        """Предоставляет шлюз для отправки email-уведомлений через SMTP."""

        async with NotificationEmailGateway(
            smtp_server=config.smtp_server,
            smtp_port=config.smtp_port,
            imap_username=config.imap_username,
            imap_password=config.imap_password,
        ) as gateway:
            yield gateway

    @provide(scope=Scope.REQUEST)
    def create_use_case(self, event: StreamMessage) -> DeduplicateEventUseCase: ...

    coordinator_publisher = provide(
        source=RabbitMQCoordinatorGateway, provides=CoordinatorGateway
    )

    tokens_gateway = provide(source=JwtTokensGateway, provides=TokensGateway)
    security_gateway = provide(source=BcryptSecurityGateway, provides=SecurityGateway)
    files_gateway = provide(source=MinioFilesGateway, provides=FilesGateway)

    telegram_notification_gateway = provide(NotificationTelegramGateway)
    notification_gateway_factory = provide(
        source=NotificationGatewayFactory,
        provides=NotificationGatewayAbstractFactory,
    )
