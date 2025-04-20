from dataclasses import dataclass
from typing import List

from domain.users.entities import User

from main_service.domain.organizations.enums import RoleEnum


@dataclass
class UpdateOrganizationDto:
    organization_id: int
    title: str
    actor: User
    roles: list[int]
    members: list[int]


@dataclass
class UpdateUserOrganizationRoleDto:
    id: int
    user_id: int
    actor: User
    role: RoleEnum
