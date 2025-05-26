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


roles_priorities = [
    RoleEnum.SUPER_USER,
    RoleEnum.SUPER_OWNER,
    RoleEnum.SUPER_ADMIN,
    RoleEnum.SUPER_REDACTOR,
    RoleEnum.OWNER,
    RoleEnum.ADMIN,
    RoleEnum.REDACTOR,
    RoleEnum.PUBLIC,
]

roles_delete_priorities = [
    RoleEnum.SUPER_USER,
    RoleEnum.SUPER_OWNER,
    RoleEnum.OWNER,
    RoleEnum.SUPER_ADMIN,
    RoleEnum.ADMIN,
    RoleEnum.SUPER_REDACTOR,
    RoleEnum.REDACTOR,
]

roles_priorities_table = {role: i for i, role in enumerate(roles_priorities)}
roles_delete_priorities_table = {
    role: i for i, role in enumerate(roles_delete_priorities)
}
