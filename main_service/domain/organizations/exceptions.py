from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from domain.organizations.entities import Organization, OrganizationToken


class OrganizationNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Organization)

    """
    Ошибка, которая возникает, если Organization был не найден | 
    read_organization
    """


class OrganizationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Organization)

    """
    Ошибка, которая возникает, если такой Organization уже существует  | 
    read_organization
    """


class OrganizationAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()

    """
    Ошибка, которая возникает, если не хавтило прав на действи | 
    update_organization, create_organization, delete_organization
    """


class OrganizationTokenNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(OrganizationToken)

    """
    Ошибка, которая возникает, если OrganizationToken был не найден | 
    read_organization_token
    """


class OrganizationTokenAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(OrganizationToken)

    """
    Ошибка, которая возникает, если такой OrganizationToken уже был создан | 
    create_organization_token
    """


class OrganizationTokenAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()

    """
    Ошибка, которая возникает, если не хватает прав на действие с OrganizationToken
    """
