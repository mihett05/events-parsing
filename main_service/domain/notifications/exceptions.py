from domain.exceptions import (
    EntityAlreadyExistsError,
    EntityException,
    EntityNotFoundError,
)
from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Notification)

    """
    Ошибка, которая возникает, если Notification был не найден | 
    read_attachment
    """


class NotificationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Notification)

    """
    Ошибка, которая возникает, если Notification уже был создан | 
    create_attachment
    """


class FailedSendNotificationError(EntityException):
    def __init__(self, user: User):
        super().__init__(f"Failed to send notification to {user}")

    """
    Ошибка, которая возникает, если Notification был не найден | 
    read_attachment
    """
