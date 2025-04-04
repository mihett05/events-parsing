from dataclasses import dataclass

from domain.organizations.enums import RoleEnum


@dataclass
class Organization:
    id: int
    title: str

    admins: list[int]
    members: list[int]


@dataclass
class UserOrganizationRole:
    id: int
    role: RoleEnum
    user_id: int
    organization_id: int
