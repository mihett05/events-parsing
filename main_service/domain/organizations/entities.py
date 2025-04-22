from dataclasses import dataclass
from datetime import datetime
from domain.organizations.enums import RoleEnum


@dataclass
class Organization:
    id: int
    created_at: datetime
    title: str
    owner_id: int
    admins: list[int]


@dataclass
class UserOrganizationRole:
    id: int
    role: RoleEnum
    user_id: int
    organization_id: int
