from domain.organizations.entities import Organization
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class OrganizationNotFoundErrorError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Organization)


class OrganizationAlreadyExistsErrorError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Organization)
