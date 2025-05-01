from dataclasses import dataclass
from datetime import datetime

from domain.organizations.enums import RoleEnum


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
    page: int | None
    page_size: int | None


@dataclass
class ReadUserOrganizationRolesDto:
    organization_id: int
    page: int
    page_size: int
