from dishka import Provider, provide, Scope

from infrastructure.config import get_config, Config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return get_config()
