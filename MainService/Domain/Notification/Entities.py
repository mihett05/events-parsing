from dataclasses import dataclass
from datetime import datetime

import MainService.Domain.Notification.Dtos as dtos

@dataclass
class Notification:
    id: int
    text: bytes
    recipient: int
    type: dtos.NotificationTypeEnum
    format: dtos.NotificationFormatEnum
    created_at: datetime