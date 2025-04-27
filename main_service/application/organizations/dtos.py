from dataclasses import dataclass
from typing import List

from domain.organizations.enums import RoleEnum
from domain.users.entities import User


@dataclass
class UpdateOrganizationDto:
    id: int
    title: str


@dataclass
class UpdateUserOrganizationRoleDto:
    id: int
    user_id: int
    role: RoleEnum
