from abc import ABCMeta

from application.auth.enums import PermissionsEnum


class PermissionProvider(metaclass=ABCMeta):
    """
    Абстрактный базовый класс для провайдеров прав доступа.

    Определяет интерфейс для получения набора разрешений.
    Реализации должны предоставлять конкретные правила проверки прав.
    """

    def __call__(self) -> set[PermissionsEnum]: ...
