from pydantic import EmailStr

from infrastructure.api.models import CamelModel


class CreateUserModelDto(CamelModel):
    email: EmailStr
    password: str
    fullname: str = ""
    is_active: bool = True


class AuthenticateUserModelDto(CamelModel):
    email: EmailStr
    password: str
