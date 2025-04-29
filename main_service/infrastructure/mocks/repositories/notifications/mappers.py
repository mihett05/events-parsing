from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
)
from domain.notifications.dtos import CreateNotificationDto
from domain.notifications.entities import Notification

from infrastructure.mocks.mappers import mock_retort

retort = mock_retort.extend(recipe=[])


map_create_dto_to_entity = retort.get_converter(
    CreateNotificationDto,
    Notification,
    recipe=[
        allow_unlinked_optional(P[Notification].id),
        allow_unlinked_optional(P[Notification].created_at),
    ],
)
