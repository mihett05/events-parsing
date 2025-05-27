from datetime import date

from domain.events.entities import Event
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationFormatEnum
from domain.notifications.repositories import NotificationsRepository


class CreateNotificationUseCase:
    """
    Юзкейс создания уведомлений о событии.

    Инкапсулирует логику формирования и сохранения уведомлений для участников события.
    Использует шаблоны для генерации текста уведомлений в разных форматах.
    """

    # TODO: Надо вынести шаблончик в сущность (с юзкейсами, инфрой и прочей херней)
    #  Чтобы у нас это можно было редактировать в админке
    __templates: dict[NotificationFormatEnum, str] = {
        NotificationFormatEnum.RAW_TEXT: (
            "Доброго времени суток {username}!\n\n"
            'Уведомляем вас о событии "{event.title}",\n'
            'которое произойдет {date} в формате "{event.format.value}"\n'
            "Вы можете отключить эту рассылку в своих настройках в личном кабинете.\n"
            "Хорошего Вам дня и удачного мероприятия!"
        )
    }

    def __init__(self, repository: NotificationsRepository):
        """
        Инициализирует юзкейс с репозиторием для работы с уведомлениями.
        """

        self.__repository = repository

    async def __call__(self, event: Event, send_date: date) -> Notification:
        """
        Основной метод юзкейса, запускающий процесс создания уведомлений.
        """

        return await self.__repository.create_many(
            await self.__create(event, send_date)
        )

    async def __create(self, event: Event, send_date: date) -> list[Notification]:
        """
        Формирует список уведомлений для всех участников события.
        """

        return [
            Notification(
                text=self.__templates[NotificationFormatEnum.RAW_TEXT].format(
                    username=user.fullname or user.email,
                    event=event,
                    date=event.start_date.strftime("%d.%m.%Y"),
                ),
                event_id=event.id,
                recipient_id=user.id,
                format=NotificationFormatEnum.RAW_TEXT,
                send_date=send_date,
            )
            for user in event.members
        ]
