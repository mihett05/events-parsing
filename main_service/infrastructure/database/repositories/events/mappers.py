from adaptix import P
from adaptix._internal.conversion.facade.provider import link_function

from domain.events.entities import Event
from infrastructure.database.mappers import postgres_retort
from .models import EventDbModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    EventDbModel,
    Event,
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda event: event.id,
            P[EventDbModel].id,
        )
    ]
)
def map_to_db(event: Event) -> EventDbModel: ...
