from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.mails.enums import MailStateEnum

from application.mails.dtos import UpdateMailDto
from application.mails.usecases import ReadMailUseCase, UpdateMailUseCase

from ..dtos import EventInfo
from .create import CreateEventUseCase
from .find import FindEventUseCase


class DeduplicateEventUseCase:
    def __init__(
        self,
        mail_read_use_case: ReadMailUseCase,
        mail_update_use_case: UpdateMailUseCase,
        event_find_use_case: FindEventUseCase,
        event_create_use_case: CreateEventUseCase,
    ):
        self.mail_read_use_case = mail_read_use_case
        self.mail_update_use_case = mail_update_use_case
        self.event_find_use_case = event_find_use_case
        self.event_create_use_case = event_create_use_case

    async def __call__(self, mail_id: int | None, dto: CreateEventDto):
        event: Event | None = await self.event_find_use_case(dto)

        if event is None:
            event: Event = await self.event_create_use_case(dto, None)

        if mail_id is not None:
            mail = await self.mail_update_use_case(
                UpdateMailDto(
                    id=mail_id,
                    state=MailStateEnum.PROCESSED,
                    event_id=event.id,
                )
            )
            return event, mail
        return event, None
