from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from domain.organizations.entities import Organization, OrganizationToken


class OrganizationNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Organization)


class OrganizationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Organization)


class OrganizationAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()


class OrganizationTokenNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(OrganizationToken)


class OrganizationTokenAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(OrganizationToken)


class OrganizationTokenAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()
