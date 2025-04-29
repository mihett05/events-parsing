from adaptix import P
from adaptix.conversion import link_function
from domain.notifications.entities import Notification

from infrastructure.api.retort import pydantic_retort

from .models import NotificationModel

retort = pydantic_retort.extend(recipe=[])

map_to_pydantic = retort.get_converter(
    Notification,
    NotificationModel,
    recipe=[
        link_function(
            lambda notification: notification.id,
            P[NotificationModel].id,
        ),
        link_function(
            lambda notification: notification.created_at,
            P[NotificationModel].created_at,
        ),
        link_function(
            lambda notification: notification.recipient_id,
            P[NotificationModel].recipient_id,
        ),
    ],
)
