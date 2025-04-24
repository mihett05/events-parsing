from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.organizations.enums import RoleEnum
from domain.users.entities import User


@dataclass
class CreateOrganizationDto:
    owner_id: int
    title: str
    created_at: datetime


@dataclass
class CreateUserOrganizationRoleDto:
    role: RoleEnum
    owner_id: int
    organization_id: int


@dataclass
class ReadOrganizationsDto:
    page: int
    page_size: int


@dataclass
class ReadUserOrganizationRolesDto:
    organization_id: int
    page: int
    page_size: int
