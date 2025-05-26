from application.auth.permissions import PermissionBuilder
from dishka import Provider, Scope, provide
from domain.users.role_getter import RoleGetter


class PermissionProvider(Provider):
    scope = Scope.REQUEST

    builder = provide(source=PermissionBuilder)

    role_getter = provide(source=RoleGetter)
