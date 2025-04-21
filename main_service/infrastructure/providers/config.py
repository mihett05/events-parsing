from application.auth.tokens.config import TokenConfig
from dishka import Provider, Scope, provide

from infrastructure.config import Config, get_config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return get_config()

    @provide(scope=Scope.APP)
    def get_token_config(self) -> TokenConfig:
        config = get_config()
        return TokenConfig(secret_key=config.secret_key)
