from domain.users.enums import RoleEnum, UserNotificationSendToEnum

from infrastructure.api.models import CamelModel


class UpdateUserModelDto(CamelModel):
    fullname: str | None = None
    telegram_id: int | None = None
    send_to_type: UserNotificationSendToEnum | None = None


class CreateUserRoleModelDto(CamelModel):
    user_id: int
    organization_id: int
    role: RoleEnum


class UpdateUserRoleModelDto(CamelModel):
    user_id: int
    organization_id: int
    role: RoleEnum
