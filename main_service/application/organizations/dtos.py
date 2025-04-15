from dataclasses import dataclass
from typing import List

from domain.users.entities import User


@dataclass
class UpdateOrganizationDto:
    organization_id: int
    title: str
    actor: User
    roles: list[int]
    members: list[int]
