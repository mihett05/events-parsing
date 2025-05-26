from adaptix import P
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
from icalendar import Calendar
from icalendar import Event as ICalEvent

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


event_user_map_to_pydantic = retort.get_converter(
    EventUser,
    EventUserModel,
    recipe=[
        coercer(Event, EventModel, map_to_pydantic),
        coercer(User, UserModel, user_map_to_pydantic),
    ],
)


def map_to_user(event_user: EventUser) -> UserModel:
    return user_map_to_pydantic(event_user.user)


def map_to_ics(events: list[Event]) -> bytes:
    cal = Calendar()
    cal.add("version", "2.0")

    for event in events:
        ical_event = ICalEvent()

        ical_event.add("summary", event.title)
        ical_event.add("dtstart", event.start_date)
        if event.location:
            ical_event.add("location", event.location)

        if event.end_date:
            ical_event.add("dtend", event.end_date)

        if event.description:
            ical_event.add("description", event.description)

        uid = (
            f"event-{event.id}@example.com"
            if event.id
            else f"event-{hash(event)}@example.com"
        )
        ical_event.add("uid", uid)

        cal.add_component(ical_event)

    return cal.to_ical()
