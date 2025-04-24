from dataclasses import dataclass
from typing import List

from domain.users.entities import User

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
