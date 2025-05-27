from datetime import datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.events.exceptions import InvalidEventPeriodError
from pydantic import BaseModel, model_validator

from infrastructure.api.models import CamelModel


def _check_dates_order(self):
    """Валидатор для проверки корректности временных периодов.

    Проверяет, что дата начала предшествует дате окончания.
    Возвращает self для цепочки вызовов.
    Вызывает InvalidEventPeriodError при нарушении порядка дат.
    """

    if self.start_date is None or self.end_date is None:
        return self

    if self.start_date > self.end_date:
        raise InvalidEventPeriodError()
    return self


class CreateEventModelDto(CamelModel):
    """Pydantic модель для создания события.

    Включает валидацию временных периодов.
    """

    title: str
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    description: str | None
    end_date: datetime
    start_date: datetime
    end_registration: datetime
    organization_id: int | None
    is_visible: bool = True

    @model_validator(mode="after")
    def _check_dates_period(self):
        """Проверяет корректность временных периодов события."""

        return _check_dates_order(self)


class UpdateEventModelDto(CamelModel):
    """Pydantic модель для обновления события."""

    title: str
    description: str
    is_visible_status: bool


class ReadAllEventsFeedModelDto(BaseModel):
    """Pydantic модель для чтения событий ленты.

    Параметры пагинации и фильтрации событий для ленты.
    Включает валидацию временных периодов фильтрации.
    """

    page: int = 0
    page_size: int = 50
    organization_id: int | None = None
    type: EventTypeEnum | None = None
    format: EventFormatEnum | None = None
    end_date: datetime | None = None
    start_date: datetime | None = None

    @model_validator(mode="after")
    def _check_dates_period(self):
        """Проверяет корректность временного периода фильтрации."""

        return _check_dates_order(self)


class ReadAllEventsCalendarModelDto(BaseModel):
    """Pydantic модель для чтения событий календаря.

    Параметры временного периода для выборки событий календаря.
    Включает валидацию временных периодов.
    """

    end_date: datetime | None = None
    start_date: datetime | None = None

    @model_validator(mode="after")
    def _check_dates_period(self):
        """Проверяет корректность временного периода выборки."""

        return _check_dates_order(self)
