from pydantic import EmailStr

from infrastructure.api.models import CamelModel
from infrastructure.api.v1.users.models import UserModel


class CreateUserModelDto(CamelModel):
    email: EmailStr
    password: str
    fullname: str = ""
    is_active: bool = True


class UserWithToken(CamelModel):
    access_token: str
    user: UserModel


class UserAuthenticate(CamelModel):
    email: EmailStr
    password: str
