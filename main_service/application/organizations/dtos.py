from dataclasses import dataclass

from domain.organizations.enums import RoleEnum


@dataclass
class UpdateOrganizationDto:
    id: int
    title: str


@dataclass
class UpdateUserOrganizationRoleDto:
    id: int
    user_id: int
    role: RoleEnum
