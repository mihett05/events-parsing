from dishka import make_async_container, AsyncContainer, Provider

from .config import ConfigProvider
from .database import DatabaseProvider
from .repositories import RepositoriesProvider
from .usecases import UseCasesProvider


def get_container_infrastructure() -> list[Provider]:
    return [
        ConfigProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
    ]


def get_container_application() -> tuple[Provider]:
    return (UseCasesProvider(),)


def create_container() -> AsyncContainer:
    return make_async_container(
        *get_container_infrastructure(),
        *get_container_application(),
    )
