from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.users.entities import User, UserOrganizationRole


class UserNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(User)


class UserRoleAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(UserOrganizationRole)


class UserRoleNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(UserOrganizationRole)
