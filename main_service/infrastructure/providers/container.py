from dishka import AsyncContainer, Provider, make_async_container

from infrastructure.config import Config, get_config

from .config import ConfigProvider
from .database import DatabaseProvider
from .gateways import GatewaysProvider
from .permissions import PermissionProvider
from .repositories import RepositoriesProvider
from .telegram_bot import BotProvider
from .usecases import UseCasesProvider


def get_container_infrastructure() -> list[Provider]:
    return [
        ConfigProvider(),
        GatewaysProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
        BotProvider(),
    ]


def get_container_application() -> list[Provider]:
    return [
        PermissionProvider(),
        UseCasesProvider(),
    ]


def create_container() -> AsyncContainer:
    return make_async_container(
        *get_container_infrastructure(),
        *get_container_application(),
        context={Config: get_config()},
    )
