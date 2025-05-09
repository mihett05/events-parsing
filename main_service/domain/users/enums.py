from enum import Enum


class UserNotificationSendToEnum(Enum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"


class RoleEnum(Enum):
    SUPER_USER = "SUPER_USER"
    SUPER_OWNER = "SUPER_AUTOBUS"
    SUPER_ADMIN = "SUPER_ADMIN"
    SUPER_REDACTOR = "SUPER_REDACTOR"
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    REDACTOR = "REDACTOR"
    PUBLIC = "PUBLIC"
