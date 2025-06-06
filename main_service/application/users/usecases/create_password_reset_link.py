import datetime

from application.transactions import TransactionsGateway
from domain.notifications.entities import Notification
from domain.users.dtos import CreatePasswordResetTokenDto
from domain.users.entities import PasswordResetToken, User
from domain.users.enums import UserNotificationSendToEnum
from domain.users.repositories import PasswordResetTokenRepository, UsersRepository
from infrastructure.config import Config

from application.notifications.factory import NotificationGatewayAbstractFactory
from application.users.dtos import ForgotPasswordDto


class CreatePasswordResetLink:
    def __init__(
        self,
        send_notification_gateway_factory: NotificationGatewayAbstractFactory,
        config: Config,
        users_repository: UsersRepository,
        token_repository: PasswordResetTokenRepository,
        tx: TransactionsGateway,
    ):
        self.__gateway_factory = send_notification_gateway_factory
        self.__config = config
        self.__users_repository = users_repository
        self.__token_repository = token_repository
        self.__transaction = tx

    def __create_notification(
        self, user: User, token: PasswordResetToken
    ) -> Notification:
        # TODO: гавно переделывай, конфиг харам
        return Notification(
            text=f"Уважаемый, {user.fullname}. "
            f"По этой ссылке вы можете изменить ваш пароль: "
            f"{self.__config.base_url}/reset/{token.id}",
            event_id=-1,
            recipient_id=user.id,
            send_date=datetime.date.today(),
        )

    async def __call__(self, dto: ForgotPasswordDto) -> PasswordResetToken:
        async with self.__transaction:
            user = await self.__users_repository.read_by_email(dto.email)
            token = await self.__token_repository.create(
                CreatePasswordResetTokenDto(user_id=user.id, user=user)
            )
            notification = self.__create_notification(user, token)
            gateway = self.__gateway_factory.get(
                user, override=UserNotificationSendToEnum.EMAIL
            )
            await gateway.send(notification, user)
            return token
