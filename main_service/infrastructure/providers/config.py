from dishka import Provider, Scope, provide

from infrastructure.config import Config, get_config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return get_config()
