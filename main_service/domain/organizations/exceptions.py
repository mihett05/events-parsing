from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.organizations.entities import Organization


class OrganizationNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Organization)


class OrganizationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Organization)
