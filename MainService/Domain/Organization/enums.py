from enum import Enum

class RoleEnum(Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    REDACTOR = "REDACTOR"
    PUBLIC = "PUBLIC"