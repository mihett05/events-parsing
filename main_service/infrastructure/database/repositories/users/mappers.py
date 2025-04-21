from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function

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
        link_function(
            lambda user: user.id,
            P[UserDatabaseModel].id,
        ),
    ]
)
def map_to_db(user: User) -> UserDatabaseModel: ...
