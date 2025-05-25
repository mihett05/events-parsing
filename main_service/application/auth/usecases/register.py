import datetime

from domain.notifications.entities import Notification
from domain.users.dtos import CreateActivationTokenDto
from domain.users.entities import User, UserActivationToken
from domain.users.enums import UserNotificationSendToEnum
from infrastructure.config import Config
from infrastructure.gateways.notifications.gateways import (
    NotificationEmailGateway,
)

from application.users.usecases.create_user_activation_token import (
    CreateUserActivationTokenUseCase,
)

from ...notifications.factory import NotificationGatewayAbstractFactory
from ..dtos import RegisterUserDto
from ..tokens.gateways import SecurityGateway
from .create_user_with_password import CreateUserWithPasswordUseCase


class RegisterUseCase:
    def __init__(
        self,
        create_user_use_case: CreateUserWithPasswordUseCase,
        security_gateway: SecurityGateway,
        send_notification_gateway_factory: NotificationGatewayAbstractFactory,
        create_activation_token_use_case: CreateUserActivationTokenUseCase,
        config: Config,
    ):
        self.gateway_factory = send_notification_gateway_factory
        self.create_user_use_case = create_user_use_case
        self.security_gateway = security_gateway
        self.create_activation_token_use_case = create_activation_token_use_case
        self.__config = config

    def __create_notification(self, user: User, token: UserActivationToken):
        return Notification(
            text=f"Уважаемый, {user.fullname}."
            f"По этой ссылке вы можете активировать ваш аккаунт: "
            f"http://{self.__config.server_host}:{self.__config.server_port}/v1/auth/activate/{token.id}",
            event_id=-1,
            recipient_id=user.id,
            send_date=datetime.date.today(),
        )

    async def __call__(self, dto: RegisterUserDto) -> UserActivationToken:
        user = await self.create_user_use_case(dto)
        token = await self.create_activation_token_use_case(
            CreateActivationTokenDto(user_id=user.id, user=user)
        )

        gateway = self.gateway_factory.get(
            user, override=UserNotificationSendToEnum.EMAIL
        )
        await gateway.send(self.__create_notification(user, token), user)
        return token
