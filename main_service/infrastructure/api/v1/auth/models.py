from infrastructure.api.models import CamelModel
from infrastructure.api.v1.users.models import UserModel


class UserWithTokenModel(CamelModel):
    """Модель ответа API, содержащая данные пользователя и его access-токен.

    Используется для возврата данных после успешной аутентификации или регистрации.
    """

    access_token: str
    user: UserModel
