from dataclasses import dataclass

from domain.organizations.enums import RoleEnum


@dataclass
class CreateOrganizationDto:
    title: str


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
