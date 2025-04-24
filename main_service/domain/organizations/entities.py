from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.organizations.enums import RoleEnum
from domain.users.entities import User


@dataclass
class Organization:
    id: int
    created_at: datetime
    title: str
    owner_id: int

@dataclass
class UserOrganizationRole:
    id: int
    role: RoleEnum
    user_id: int
    organization_id: int
