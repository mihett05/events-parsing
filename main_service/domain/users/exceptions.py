from domain.exceptions import EntityAlreadyExists, EntityNotFound
from domain.users.entities import User


class UserNotFound(EntityNotFound):
    def __init__(self):
        super().__init__(User)


class UserAlreadyExists(EntityAlreadyExists):
    def __init__(self):
        super().__init__(User)
