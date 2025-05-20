from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.mails.enums import MailStateEnum
from domain.users.entities import User

from application.mails.dtos import UpdateMailDto
from application.mails.usecases import ReadMailUseCase, UpdateMailUseCase

from .create import CreateEventUseCase
from .find import FindEventUseCase


class DeduplicateEventUseCase:
    def __init__(
        self,
        mail_read_use_case: ReadMailUseCase,
        mail_update_use_case: UpdateMailUseCase,
        event_find_use_case: FindEventUseCase,
        event_create_use_case: CreateEventUseCase,
        super_user: User,
    ):
        self.__mail_read_use_case = mail_read_use_case
        self.__mail_update_use_case = mail_update_use_case
        self.__event_find_use_case = event_find_use_case
        self.__event_create_use_case = event_create_use_case
        self.__super_user = super_user

    async def __call__(self, mail_id: int | None, dto: CreateEventDto):
        event: Event | None = await self.__event_find_use_case(dto)

        if event is None:
            event: Event = await self.__event_create_use_case(dto, self.__super_user)

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
