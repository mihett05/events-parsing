from adaptix import P
from adaptix.conversion import link_function

from application.auth.dtos import AuthenticateUserDto, RegisterUserDTO
from application.auth.dtos import AuthenticateUserDto
from domain.users.dtos import CreateUserDto

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
)

retort = pydantic_retort.extend(recipe=[])

map_authenticate_dto_from_pydantic = retort.get_converter(
    AuthenticateUserModelDto,
    AuthenticateUserDto,
    recipe=[
        link_function(
            lambda user: user.email,
            P[AuthenticateUserDto].email,
        ),
    ],
)

map_create_dto_from_pydantic = retort.get_converter(
    CreateUserModelDto,
    RegisterUserDTO,
    recipe=[
        link_function(
            lambda user: user.email,
            P[RegisterUserDTO].email,
        ),
    ],
)
