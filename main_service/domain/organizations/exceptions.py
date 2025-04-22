from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.organizations.entities import Organization


class OrganizationNotFoundErrorError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Organization)


class OrganizationAlreadyExistsErrorError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Organization)
