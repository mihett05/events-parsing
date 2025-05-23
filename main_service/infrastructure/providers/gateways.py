import logging
from typing import AsyncIterable

from application.attachments.gateways import FilesGateway
from application.auth.tokens.gateways import SecurityGateway, TokensGateway
from application.events.coordinator.gateway import CoordinatorGateway
from application.events.usecases import DeduplicateEventUseCase
from application.mails.gateway import EmailsGateway
from dishka import Provider, Scope, provide
from faststream.broker.message import StreamMessage
from faststream.rabbit import RabbitBroker
from miniopy_async import Minio

from infrastructure.auth.bcrypt import BcryptSecurityGateway
from infrastructure.auth.jwt import JwtTokensGateway
from infrastructure.config import Config
from infrastructure.imap.gateway import ImapEmailsGateway
from infrastructure.media.attachments.minio import MinioFilesGateway
from infrastructure.rabbit.events import (
    RabbitMQCoordinatorGateway,
)


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide
    def broker(self, config: Config) -> RabbitBroker:
        return RabbitBroker(config.rabbitmq_url, log_level=logging.DEBUG)

    @provide
    def minio(self, config: Config) -> Minio:
        return Minio(
            endpoint=config.minio_url,
            access_key=config.minio_root_user,
            secret_key=config.minio_root_password,
            secure=False,
        )

    @provide(scope=Scope.REQUEST)
    async def emails_gateway(
        self, config: Config
    ) -> AsyncIterable[EmailsGateway]:
        async with ImapEmailsGateway(
            imap_server=config.imap_server,
            imap_username=config.imap_username,
            imap_password=config.imap_password,
        ) as gateway:
            yield gateway

    @provide(scope=Scope.REQUEST)
    def create_use_case(
        self, event: StreamMessage
    ) -> DeduplicateEventUseCase: ...

    coordinator_publisher = provide(
        source=RabbitMQCoordinatorGateway, provides=CoordinatorGateway
    )

    tokens_gateway = provide(source=JwtTokensGateway, provides=TokensGateway)
    security_gateway = provide(
        source=BcryptSecurityGateway, provides=SecurityGateway
    )
    files_gateway = provide(source=MinioFilesGateway, provides=FilesGateway)
