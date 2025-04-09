from dishka import AsyncContainer, Provider, make_async_container

from .config import ConfigProvider
from .database import DatabaseProvider
from .gateways import GatewaysProvider
from .permissions import PermissionProvider
from .repositories import RepositoriesProvider
from .usecases import UseCasesProvider


def get_container_infrastructure() -> list[Provider]:
    return [
        PermissionProvider(),
        ConfigProvider(),
        GatewaysProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
    ]


def get_container_application() -> list[Provider]:
    return [
        UseCasesProvider(),
    ]


def create_container() -> AsyncContainer:
    return make_async_container(
        *get_container_infrastructure(),
        *get_container_application(),
    )
