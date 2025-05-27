from domain.users.enums import RoleEnum

from infrastructure.api.models import CamelModel


class UpdateUserModelDto(CamelModel):
    """
    Модель данных для обновления информации о пользователе.
    """

    fullname: str
    telegram_id: int | None = None


class CreateUserRoleModelDto(CamelModel):
    """
    Модель данных для назначения роли пользователю в организации.
    """

    user_id: int
    organization_id: int

    role: RoleEnum


class UpdateUserRoleModelDto(CamelModel):
    """
    Модель данных для изменения роли пользователя в организации.
    """

    user_id: int
    organization_id: int
    role: RoleEnum
