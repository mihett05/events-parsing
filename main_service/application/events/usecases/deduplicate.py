from collections import namedtuple

from application.events.dtos import EventInfo
from application.events.usecases import FindEventUseCase, CreateEventUseCase
from application.mails.dtos import UpdateMailDto
from application.mails.usecases import ReadMailUseCase, UpdateMailUseCase
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.mails.entities import Mail
from domain.mails.enums import MailStateEnum

pair = namedtuple("pair", ["mail", "event"])


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

    async def __call__(self, dto: EventInfo) -> pair:
        event: Event | None = await self.event_find_use_case(dto)

        if event is None:
            create_dto = CreateEventDto(
                title=dto.title or "",
                description=dto.description or "",
                organization_id=-1,
                end_date=dto.dates.end_date,
                start_date=dto.dates.start_date,
                end_registration=dto.dates.end_registration,
            )
            event: Event = await self.event_create_use_case(create_dto)

        mail: Mail = await self.mail_update_use_case(
            UpdateMailDto(
                id=dto.mail_id,
                state=MailStateEnum.PROCESSED,
                event_id=event.id,
            )
        )
        return pair(mail=mail, event=event)
