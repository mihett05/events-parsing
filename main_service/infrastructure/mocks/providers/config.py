from application.auth.tokens.config import TokenConfig
from dishka import Provider, Scope, provide

from infrastructure.config import Config, get_mock_config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return get_mock_config()

    @provide(scope=Scope.APP)
    def get_token_config(self) -> TokenConfig:
        config = get_mock_config()
        return TokenConfig(secret_key=config.secret_key)
