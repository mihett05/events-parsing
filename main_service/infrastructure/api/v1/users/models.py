from datetime import datetime

from domain.users.enums import RoleEnum

from infrastructure.api.models import CamelModel


class UserModel(CamelModel):
    id: int
    email: str

    fullname: str
    is_active: bool

    telegram_id: int | None
    created_at: datetime


class UserRoleModel(CamelModel):
    user_id: int
    organization_id: int

    role: RoleEnum
