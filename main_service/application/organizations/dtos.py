from dataclasses import dataclass


@dataclass
class UpdateOrganizationDto:
    id: int
    title: str
