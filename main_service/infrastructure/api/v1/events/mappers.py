from adaptix import P
from adaptix.conversion import coercer, link_function
from application.events.dtos import UpdateEventDto
from domain.attachments.entities import Attachment
from domain.events.dtos import CreateEventDto
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
    UpdateEventModelDto,
)
from .models import EventModel, EventUserModel

retort = pydantic_retort.extend(recipe=[])

map_create_dto_from_pydantic = retort.get_converter(CreateEventModelDto, CreateEventDto)

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
        )
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateEventModelDto,
    event_id: int,  # noqa
) -> UpdateEventDto: ...
