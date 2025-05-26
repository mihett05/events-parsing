from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from domain.users.entities import TelegramToken, User, UserOrganizationRole


class UserNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(User)


class UserAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()


class TelegramTokenNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(TelegramToken)


class TelegramTokenAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(TelegramToken)


class UserRoleAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(UserOrganizationRole)


class UserRoleNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(UserOrganizationRole)


class CalendarUUIDNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)
