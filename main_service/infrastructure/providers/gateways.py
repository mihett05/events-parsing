import logging

from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from application.events.coordinator.gateway import CoordinatorGateway
from infrastructure.api.gateways.events.publisher import (
    RabbitMQCoordinatorGatewayPublisher,
)
from infrastructure.config import Config


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide
    def broker(self, config: Config) -> RabbitBroker:
        return RabbitBroker(config.rabbitmq_url, log_level=logging.DEBUG)

    coordinator_publisher = provide(
        source=RabbitMQCoordinatorGatewayPublisher, provides=CoordinatorGateway
    )
