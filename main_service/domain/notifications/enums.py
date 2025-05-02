from enum import Enum


class NotificationTypeEnum(Enum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"


class NotificationFormatEnum(Enum):
    HTML = "HTML"
    RAW_TEXT = "RAW_TEXT"
    MARKDOWN = "MARKDOWN"


class NotificationStatusEnum(Enum):
    SENT = "SENT"
    FAILED = "FAILED"
    UNSENT = "UNSENT"
