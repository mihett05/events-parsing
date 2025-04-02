from dishka import Provider, Scope, provide

from application.auth.permissions import PermissionBuilder


class PermissionProvider(Provider):
    scope = Scope.REQUEST

    builder = provide(source=PermissionBuilder)
