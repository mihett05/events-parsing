from adaptix import P
from adaptix.conversion import link_function
from application.users.dtos import UpdateUserDto
from domain.users.entities import User

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    UpdateUserModelDto,
)
from .models import UserModel

retort = pydantic_retort.extend(recipe=[])

map_to_pydantic = retort.get_converter(
    User,
    UserModel,
    recipe=[
        link_function(
            lambda user: user.id,
            P[UserModel].id,
        )
    ],
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, user_id: user_id,
            P[UpdateUserDto].user_id,
        )
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateUserModelDto, user_id: int
) -> UpdateUserDto: ...
