from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
    coercer,
    link_function,
)
from domain.attachments.entities import Attachment
from domain.events.dtos import CreateEventDto, CreateEventUserDto
from domain.events.entities import Event, EventUser
from domain.users.entities import User

from infrastructure.database.mappers import postgres_retort
from infrastructure.database.repositories.attachments.mappers import (
    map_from_db as attachment_map_from_db,
)
from infrastructure.database.repositories.attachments.mappers import (
    map_to_db as attachment_map_to_db,
)
from infrastructure.database.repositories.users.mappers import (
    map_from_db as user_map_from_db,
)
from infrastructure.database.repositories.users.mappers import (
    map_to_db as user_map_to_db,
)

from ..attachments import AttachmentDatabaseModel
from ..users import UserDatabaseModel
from .models import EventDatabaseModel, EventUserDatabaseModel

retort = postgres_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        coercer(AttachmentDatabaseModel, Attachment, attachment_map_from_db),
        link_function(
            lambda event, is_greed: [
                user_map_from_db(member) for member in event.members
            ]
            if is_greed
            else [],
            P[Event].members,
        ),
    ],
)
def map_from_db(
    model: EventDatabaseModel,
    is_greed: bool = False,
) -> Event: ...


"""Преобразует модель события из базы данных в доменную сущность.

При is_greed=True дополнительно загружает связанных пользователей.
"""


map_to_db = retort.get_converter(
    Event,
    EventDatabaseModel,
    recipe=[
        link_function(
            lambda event: event.id,
            P[EventDatabaseModel].id,
        ),
        link_function(
            lambda event: event.created_at,
            P[EventDatabaseModel].created_at,
        ),
        coercer(Attachment, AttachmentDatabaseModel, attachment_map_to_db),
        coercer(User, UserDatabaseModel, user_map_to_db),
    ],
)
"""Конвертер для преобразования доменной сущности события в модель базы данных."""


map_create_dto_to_model = retort.get_converter(
    CreateEventDto,
    EventDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[EventDatabaseModel].id),
        allow_unlinked_optional(P[EventDatabaseModel].is_visible),
        allow_unlinked_optional(P[EventDatabaseModel].created_at),
        allow_unlinked_optional(P[EventDatabaseModel].attachments),
        allow_unlinked_optional(P[EventDatabaseModel].members),
        link_function(
            lambda dto: dto.organization_id,
            P[EventDatabaseModel].organization_id,
        ),
    ],
)
"""Конвертер для преобразования DTO создания события в модель базы данных."""

event_user_map_from_db = retort.get_converter(
    EventUserDatabaseModel,
    EventUser,
    recipe=[
        coercer(UserDatabaseModel, User, user_map_from_db),
        coercer(EventDatabaseModel, Event, map_from_db),
    ],
)
"""Конвертер для преобразования модели связи пользователя и события из базы данных в доменную сущность."""

event_user_map_to_db = retort.get_converter(
    EventUser,
    EventUserDatabaseModel,
    recipe=[
        coercer(User, UserDatabaseModel, user_map_to_db),
        coercer(Event, EventDatabaseModel, map_to_db),
    ],
)
"""Конвертер для преобразования доменной сущности связи пользователя и события в модель базы данных."""

event_user_map_dto = retort.get_converter(
    CreateEventUserDto,
    EventUserDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[EventUserDatabaseModel].user),
        allow_unlinked_optional(P[EventUserDatabaseModel].event),
    ],
)
"""Конвертер для преобразования DTO создания связи пользователя и события в модель базы данных."""
