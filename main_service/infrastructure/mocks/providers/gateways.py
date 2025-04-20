import logging

from application.events.coordinator.gateway import CoordinatorGateway
from application.events.usecases import DeduplicateEventUseCase
from dishka import Provider, Scope, provide
from faststream.broker.message import StreamMessage
from faststream.rabbit import RabbitBroker

from infrastructure.config import Config
from infrastructure.mocks.gateways.events.gateway import (
    MemoryCoordinatorGateway,
)
from infrastructure.rabbit.events import (
    RabbitMQCoordinatorGateway,
)


class GatewaysProvider(Provider):
    scope = Scope.APP

    coordinator_publisher = provide(
        source=MemoryCoordinatorGateway, provides=CoordinatorGateway
    )
