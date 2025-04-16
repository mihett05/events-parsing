import logging

from dishka import Provider, Scope, provide
from faststream.broker.message import StreamMessage
from faststream.rabbit import RabbitBroker

from application.events.coordinator.gateway import CoordinatorGateway
from application.events.usecases import DeduplicateEventUseCase
from infrastructure.config import Config
from infrastructure.rabbit.events import (
    RabbitMQCoordinatorGateway,
)


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide
    def broker(self, config: Config) -> RabbitBroker:
        return RabbitBroker(config.rabbitmq_url, log_level=logging.DEBUG)

    @provide(scope=Scope.REQUEST)
    def create_use_case(
        self, event: StreamMessage
    ) -> DeduplicateEventUseCase: ...

    coordinator_publisher = provide(
        source=RabbitMQCoordinatorGateway, provides=CoordinatorGateway
    )
