from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function
from application.auth.dtos import AuthenticateUserDto, RegisterUserDto
from application.users.dtos import ForgotPasswordDto, UpdateUserPasswordDto

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    AuthenticateUserModelDto,
    CreateNewPasswordModelDto,
    CreateUserModelDto,
    UpdateUserPasswordModelDto,
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
"""Конвертер для трансформации модели аутентификации API в DTO для слоя приложения."""

map_create_dto_from_pydantic = retort.get_converter(
    CreateUserModelDto,
    RegisterUserDto,
    recipe=[
        link_function(
            lambda user: user.email,
            P[RegisterUserDto].email,
        ),
        allow_unlinked_optional(P[RegisterUserDto].is_active),
    ],
)
"""Конвертер для трансформации модели регистрации API в DTO для слоя приложения с поддержкой опциональных полей."""

map_forgot_password_dto_from_pydantic = retort.get_converter(
    CreateNewPasswordModelDto,
    ForgotPasswordDto,
    recipe=[
        link_function(
            lambda dto: dto.email,
            P[ForgotPasswordDto].email,
        )
    ],
)


map_update_password_dto_from_pydantic = retort.get_converter(
    UpdateUserPasswordModelDto,
    UpdateUserPasswordDto,
    recipe=[
        link_function(
            lambda dto: dto.password,
            P[UpdateUserPasswordModelDto].password,
        )
    ],
)
