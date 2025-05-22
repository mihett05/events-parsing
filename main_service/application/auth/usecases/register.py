import datetime

from domain.notifications.entities import Notification
from domain.users.dtos import CreateActivationTokenDto
from domain.users.entities import User, UserActivationToken
from infrastructure.config import Config
from infrastructure.gateways.notifications.gateways import (
    NotificationEmailGateway,
)

from application.users.usecases import CreateUserUseCase
from application.users.usecases.create_user_activation_token import (
    CreateUserActivationTokenUseCase,
)

from ..dtos import RegisterUserDTO
from ..tokens.gateways import SecurityGateway


class RegisterUseCase:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        security_gateway: SecurityGateway,
        send_notification_gateway: NotificationEmailGateway,
        create_activation_token_use_case: CreateUserActivationTokenUseCase,
        config: Config,
    ):
        self.send_notification_gateway = send_notification_gateway
        self.create_user_use_case = create_user_use_case
        self.security_gateway = security_gateway
        self.create_activation_token_use_case = create_activation_token_use_case
        self.__config = config

    def __create_notification(self, user: User, token: UserActivationToken):
        return Notification(
            text=f"Уважаемый, {user.fullname}."
            f"По этой ссылке вы можете активировать ваш аккаунт: "
            f"https://{self.__config.server_host}/activate/{token.id}",
            event_id=-1,
            recipient_id=user.id,
            send_date=datetime.date.today(),
        )

    async def __call__(self, dto: RegisterUserDTO) -> UserActivationToken:
        password_dto = self.security_gateway.create_hashed_password(dto.password)
        user = User(
            email=dto.email,
            fullname=dto.fullname,
            salt=password_dto.salt,
            hashed_password=password_dto.hashed_password,
            is_active=False,
        )

        user = await self.create_user_use_case(user)
        token = await self.create_activation_token_use_case(
            CreateActivationTokenDto(user_id=user.id)
        )
        async with self.send_notification_gateway as gateway:
            await gateway.send(self.__create_notification(user, token), user)
        return token
