from enum import Enum


class PermissionsEnum(Enum):
    # Event region
    CAN_READ_EVENT = "CAN_READ_EVENT"
    CAN_UPDATE_EVENT = "CAN_UPDATE_EVENT"
    CAN_DELETE_EVENT = "CAN_DELETE_EVENT"
    CAN_SET_OWNER = "CAN_SET_OWNER"
