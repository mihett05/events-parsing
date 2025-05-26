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


class NotificationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Notification)


class FailedSendNotificationError(EntityException):
    def __init__(self, user: User):
        super().__init__(f"Failed to send notification to {user}")
