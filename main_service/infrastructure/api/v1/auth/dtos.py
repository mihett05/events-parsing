from pydantic import EmailStr

from infrastructure.api.models import CamelModel


class CreateUserModelDto(CamelModel):
    """
    Модель данных для создания нового пользователя.
    """

    email: EmailStr
    password: str
    fullname: str = ""


class AuthenticateUserModelDto(CamelModel):
    """
    Модель данных для аутентификации пользователя.
    """

    email: EmailStr
    password: str
