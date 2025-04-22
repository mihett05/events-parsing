<<<<<<< HEAD
import logging

from application.events.coordinator.gateway import CoordinatorGateway
from application.events.usecases import DeduplicateEventUseCase
from dishka import Provider, Scope, provide
from faststream.broker.message import StreamMessage
from faststream.rabbit import RabbitBroker

from infrastructure.config import Config
=======
from application.auth.tokens.gateways import SecurityGateway, TokensGateway
from application.events.coordinator.gateway import CoordinatorGateway
from dishka import Provider, Scope, provide

from infrastructure.auth.bcrypt import BcryptSecurityGateway
from infrastructure.auth.jwt import JwtTokensGateway
>>>>>>> 734238dad51cb720fbb31b35c5efe9ed046573b5
from infrastructure.mocks.gateways.events.gateway import (
    MemoryCoordinatorGateway,
)


class GatewaysProvider(Provider):
    scope = Scope.APP

    coordinator_publisher = provide(
        source=MemoryCoordinatorGateway, provides=CoordinatorGateway
    )
    tokens_gateway = provide(source=JwtTokensGateway, provides=TokensGateway)
    security_gateway = provide(
        source=BcryptSecurityGateway, provides=SecurityGateway
    )
