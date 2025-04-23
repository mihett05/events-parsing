from domain.notifications.entities import Notification
from domain.exceptions import EntityNotFoundError, EntityAlreadyExistsError


class NotificationNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Notification)


class NotificationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Notification)
