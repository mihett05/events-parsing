from dataclasses import dataclass
from datetime import datetime

import domain.notifications.enums as enums


@dataclass
class Notification:
    id: int
    text: bytes
    recipient: int
    type: enums.NotificationTypeEnum
    format: enums.NotificationFormatEnum
    created_at: datetime
