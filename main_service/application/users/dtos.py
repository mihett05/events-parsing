from dataclasses import dataclass


@dataclass
class UpdateUserDto:
    user_id: int
    fullname: str | None = None
    telegram_id: int | None = None


@dataclass
class DeleteUserRoleDto:
    user_id: int
    organization_id: int
