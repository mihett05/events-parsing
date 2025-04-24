from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.notifications.entities import Notification


class NotificationNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Notification)


class NotificationAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Notification)
