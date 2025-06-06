from dishka import (
    AsyncContainer,
    Provider,
    make_async_container,
)

from infrastructure.config import Config, get_mock_config, get_tests_config
from infrastructure.providers.container import (
    get_container_application,
    get_container_infrastructure,
)

from .config import ConfigProvider
from .gateways import GatewaysProvider
from .repositories import RepositoriesProvider
from .transactions import TransactionsProvider


def get_container_mocks() -> list[Provider]:
    return [
        ConfigProvider(),
        GatewaysProvider(),
        TransactionsProvider(),
        RepositoriesProvider(),
    ]


def create_unittest_container(config: Config | None = None) -> AsyncContainer:
    if not config:
        config = get_mock_config()
    return make_async_container(
        *get_container_mocks(),
        *get_container_application(),
        context={Config: config},
    )


def create_integration_test_container(
    config: Config | None = None,
) -> AsyncContainer:
    if not config:
        config = get_tests_config()
    return make_async_container(
        *get_container_infrastructure(),
        *get_container_application(),
        context={Config: config},
    )
