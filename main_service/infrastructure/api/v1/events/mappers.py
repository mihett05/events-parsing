from adaptix import P
from adaptix._internal.conversion.facade.provider import allow_unlinked_optional
from adaptix.conversion import coercer, link_function
from application.events.dtos import UpdateEventDto
from domain.attachments.entities import Attachment
from domain.events.dtos import (
    CreateEventDto,
    ReadAllEventsDto,
    ReadAllEventsFeedDto,
)
from domain.events.entities import Event, EventUser
from domain.users.entities import User

from infrastructure.api.retort import pydantic_retort
from infrastructure.api.v1.attachments.mappers import (
    map_to_pydantic as attachment_map_to_pydantic,
)
from infrastructure.api.v1.users.mappers import (
    map_to_pydantic as user_map_to_pydantic,
)

from ..attachments.models import AttachmentModel
from ..users.models import UserModel
from .dtos import (
    CreateEventModelDto,
    ReadAllEventsCalendarModelDto,
    ReadAllEventsFeedModelDto,
    UpdateEventModelDto,
)
from .models import EventModel, EventUserModel

retort = pydantic_retort.extend(recipe=[])

map_create_dto_from_pydantic = retort.get_converter(CreateEventModelDto, CreateEventDto)
map_read_all_dto_from_pydantic = retort.get_converter(
    ReadAllEventsFeedModelDto,
    ReadAllEventsFeedDto,
)
"""
map_read_all_dto_calendar_from_pydantic = retort.get_converter(
    ReadAllEventsCalendarModelDto,
    ReadAllEventsDto,
    recipe=[
        allow_unlinked_optional(P[ReadAllEventsDto].page),
        allow_unlinked_optional(P[ReadAllEventsDto].page_size),
        allow_unlinked_optional(P[ReadAllEventsDto].for_update),
    ],
)"""

event_user_map_to_pydantic = retort.get_converter(EventUser, EventUserModel)

map_to_pydantic = retort.get_converter(
    Event,
    EventModel,
    recipe=[
        link_function(
            lambda event: event.id,
            P[EventModel].id,
        ),
        link_function(
            lambda event: event.created_at,
            P[EventModel].created_at,
        ),
        link_function(
            lambda event: event.organization_id,
            P[EventModel].organization_id,
        ),
        coercer(Attachment, AttachmentModel, attachment_map_to_pydantic),
        coercer(User, UserModel, user_map_to_pydantic),
    ],
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, event_id: event_id,
            P[UpdateEventDto].event_id,
        ),
        link_function(
            lambda dto, is_visible_status: is_visible_status,
            P[UpdateEventDto].is_visible,
        ),
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateEventModelDto,  # noqa
    event_id: int,  # noqa
) -> UpdateEventDto: ...
