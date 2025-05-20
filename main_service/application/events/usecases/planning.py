from datetime import date, datetime

from domain.events.dtos import ReadAllEventsDto

from application.events.usecases.read_all import ReadAllEventUseCase
from application.notifications.usecases import CreateNotificationUseCase
from application.transactions import TransactionsGateway


class PlanningEventsNotificationsUseCase:
    def __init__(
        self,
        transaction: TransactionsGateway,
        read_events: ReadAllEventUseCase,
        create_notifications: CreateNotificationUseCase,
    ):
        self.__transaction = transaction
        self.__read_events = read_events
        self.__create_notifications = create_notifications

    async def __call__(
        self, event_start_date: datetime, notification_send_date: date
    ):
        dto = ReadAllEventsDto(
            page=0, page_size=50, start_date=event_start_date, for_update=True
        )

        async with self.__transaction:
            while events := await self.__read_events(dto):
                for event in events:
                    await self.__create_notifications(
                        event, notification_send_date
                    )

                dto.page += 1
