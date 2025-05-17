from domain.users.enums import RoleEnum

from infrastructure.api.models import CamelModel


class UpdateUserModelDto(CamelModel):
    fullname: str
    telegram_id: int | None = None


class CreateUserRoleModelDto(CamelModel):
    user_id: int
    organization_id: int

    role: RoleEnum


class UpdateUserRoleModelDto(CamelModel):
    user_id: int
    organization_id: int
    role: RoleEnum
