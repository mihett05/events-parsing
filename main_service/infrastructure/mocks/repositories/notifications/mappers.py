from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
)

from domain.notifications.dtos import CreateNotificationDto
from domain.notifications.entities import Notification

from infrastructure.mocks.mappers import mock_retort

retort = mock_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[Notification].id),
        allow_unlinked_optional(P[Notification].created_at),
        allow_unlinked_optional(P[Notification].recipient),
    ]
)
def map_create_dto_to_entity(dto: CreateNotificationDto) -> Notification: ...
