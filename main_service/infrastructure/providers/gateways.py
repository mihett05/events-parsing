from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from application.events.coordinator.gateway import CoordinatorGateway
from infrastructure.api.gateways.events.publisher import (
    RabbitMQCoordinatorGatewayPublisher,
)
from infrastructure.api.gateways.events.subscriber import (
    RabbitMQCoordinatorGatewaySubscriber,
)


class GatewaysProvider(Provider):
    scope = Scope.APP

    broker = provide(
        source=RabbitBroker
    )
    coordinator_publisher = provide(
        source=RabbitMQCoordinatorGatewayPublisher, provides=CoordinatorGateway
    )
    coordinator_subscriber = provide(
        source=RabbitMQCoordinatorGatewaySubscriber
    )
