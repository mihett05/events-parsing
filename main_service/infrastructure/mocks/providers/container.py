from dishka import AsyncContainer, Provider, make_async_container

from infrastructure.providers.config import ConfigProvider
from infrastructure.providers.container import get_container_application

from .repositories import RepositoriesProvider
from .transactions import TransactionsProvider


def get_container_mocks() -> list[Provider]:
    return [
        ConfigProvider(),
        TransactionsProvider(),
        RepositoriesProvider(),
    ]


def create_test_container() -> AsyncContainer:
    return make_async_container(
        *get_container_mocks(),
        *get_container_application(),
    )
