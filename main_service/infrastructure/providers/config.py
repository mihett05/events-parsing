from application.auth.tokens.config import TokenConfig
from dishka import Provider, Scope, from_context, provide
from dishka import Provider, Scope, provide
from domain.users.entities import User

from infrastructure.config import Config, get_config


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_token_config(self) -> TokenConfig:
        config = get_config()
        return TokenConfig(secret_key=config.secret_key)

    @provide(scope=Scope.APP)
    def get_super_user(self) -> User:
        return User(id=0, fullname="", email="")
