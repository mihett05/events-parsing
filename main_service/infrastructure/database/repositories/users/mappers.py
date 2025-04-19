from adaptix import P
from adaptix.conversion import allow_unlinked_optional
from domain.users.entities import User

from infrastructure.database.mappers import postgres_retort

from .models import UserDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    UserDatabaseModel,
    User,
)


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[User].salt),
        allow_unlinked_optional(P[User].created_at),
        allow_unlinked_optional(P[User].hashed_password),
    ]
)
def map_to_db(user: User) -> UserDatabaseModel: ...
