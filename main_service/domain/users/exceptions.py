from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityException,
    EntityNotFoundError,
)
from domain.users.entities import TelegramToken, User, UserOrganizationRole, PasswordResetToken


class UserNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)

    """
    Ошибка, которая возникает, если User не был найден | read_user
    """


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(User)

    """
    Ошибка, которая возникает, если такой User уже был создан | create_user
    """


class UserAccessDenied(EntityAccessDenied):
    def __init__(self):
        super().__init__()

    """
    Ошибка, которая возникает, если на действие с User не хватило прав 
    delete_user, create_role, delete_role, update_role
    """


class UserNotValidated(EntityException):
    def __init__(self):
        super().__init__(f"Пользователь не активирован!")

    """
    Ошибка, которая возникает, если User не активирован (имеет is_activa=False) 
        /auth/authentificate.py
    """


class TelegramTokenNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(TelegramToken)

    """
    Ошибка, которая возникает, если TelegramToken не найден
        connect_telegram.py
    """


class TelegramTokenAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(TelegramToken)

    """
    Ошибка, которая возникает, если такой TelegramToken уже есть
            infrastructure/database/repository.py
    """


class UserRoleAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(UserOrganizationRole)

    """
    Ошибка, которая возникает, если такой UserRole уже есть
            infrastructure/database/repository.py
    """


class UserRoleNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(UserOrganizationRole)

    """
    Ошибка, которая возникает, если UserRole не найден
          delete_role read_role infrastructure/database/repository.py
    """


class CalendarUUIDNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)

    """
        Ошибка, которая возникает, если CalendarUUID не найден (для Ical)
              delete_calendar_link.py
    """


class TelegramNotConnectedError(EntityException):
    def __init__(self):
        super().__init__("Telegram not connected")

    """
        Ошибка, которая возникает, если юзер не подключал Telegram
            update_user_use_case.py
    """

class PasswordResetTokenAlreadyUsedError(EntityAccessDenied):
    def __init__(self):
        super().__init__()