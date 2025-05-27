from dataclasses import dataclass


@dataclass
class UpdateUserDto:
    """
    Data Transfer Object для обновления данных пользователя.

    Позволяет частично обновлять информацию о пользователе.
    Все поля являются опциональными, кроме обязательного user_id.
    """

    user_id: int
    fullname: str | None = None
    telegram_id: int | None = None


@dataclass
class DeleteUserRoleDto:
    """
    Data Transfer Object для удаления роли пользователя в организации.

    Содержит идентификаторы, необходимые для однозначного определения
    связи пользователя с организацией.
    """

    user_id: int
    organization_id: int
