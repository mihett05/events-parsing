from dataclasses import dataclass


@dataclass
class UpdateUserDto:
    """DTO для обновления данных пользователя."""

    user_id: int
    fullname: str | None = None
    telegram_id: int | None = None


@dataclass
class DeleteUserRoleDto:
    """DTO для удаления роли пользователя в организации."""


    user_id: int
    organization_id: int
