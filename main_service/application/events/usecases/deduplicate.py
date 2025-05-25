from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.mails.enums import MailStateEnum
from domain.users.entities import User
from domain.users.repositories import UsersRepository
from infrastructure.config import Config

from application.mails.dtos import UpdateMailDto
from application.mails.usecases import ReadMailUseCase, UpdateMailUseCase

from .create import CreateEventUseCase
from .find import FindEventUseCase
from ...transactions import TransactionsGateway


class DeduplicateEventUseCase:
    def __init__(
        self,
        transaction: TransactionsGateway,
        mail_read_use_case: ReadMailUseCase,
        mail_update_use_case: UpdateMailUseCase,
        event_find_use_case: FindEventUseCase,
        event_create_use_case: CreateEventUseCase,
        users_repository: UsersRepository,
        config: Config,
    ):
        self.__transaction = transaction
        self.__mail_read_use_case = mail_read_use_case
        self.__mail_update_use_case = mail_update_use_case
        self.__event_find_use_case = event_find_use_case
        self.__event_create_use_case = event_create_use_case
        self.__users_repository = users_repository
        self.__config = config

    async def __call__(self, mail_id: int | None, dto: CreateEventDto):
        async with self.__transaction.nested():
            event: Event | None = await self.__event_find_use_case(dto)
            super_user = await self.__users_repository.read_by_email(
                self.__config.admin_username
            )
            if event is None:
                event: Event = await self.__event_create_use_case(dto, super_user)

            if mail_id is not None:
                mail = await self.__mail_update_use_case(
                    UpdateMailDto(
                        id=mail_id,
                        state=MailStateEnum.PROCESSED,
                        event_id=event.id,
                    )
                )
                return event, mail
            return event, None
