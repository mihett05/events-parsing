from dataclasses import dataclass


@dataclass
class UpdateOrganizationDto:
    """
    Data Transfer Object для обновления информации об организации.
    """

    id: int
    title: str
