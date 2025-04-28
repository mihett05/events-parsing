from application.auth.permissions import PermissionBuilder
from dishka import Provider, Scope, provide


class PermissionProvider(Provider):
    scope = Scope.REQUEST

    builder = provide(source=PermissionBuilder)
