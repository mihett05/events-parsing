from infrastructure.api.models import CamelModel
from infrastructure.api.v1.users.models import UserModel


class UserWithTokenModel(CamelModel):
    access_token: str
    user: UserModel
