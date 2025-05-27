from datetime import date, datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum

from infrastructure.api.models import CamelModel
from infrastructure.api.v1.attachments.models import AttachmentModel
from infrastructure.api.v1.organizations.models import OrganizationModel
from infrastructure.api.v1.users.models import UserModel


class EventModel(CamelModel):
    """Pydantic модель для представления данных о событии.

    Использует camelCase для совместимости с внешними API.
    Содержит полную информацию о событии, включая связанные сущности.
    """

    id: int
    title: str
    type: EventTypeEnum
    format: EventFormatEnum
    created_at: datetime
    organization_id: int | None = None

    is_visible: bool
    location: str | None
    description: str | None

    attachments: list[AttachmentModel]
    members: list[UserModel]

    start_date: date
    end_date: date | None
    end_registration: date | None = None


class FilterModel(CamelModel):
    """Pydantic модель для параметров фильтрации событий.

    Содержит списки допустимых значений для фильтрации по типу,
    формату и организациям. Использует camelCase для API.
    """

    type: list[EventTypeEnum]
    format: list[EventFormatEnum]
    organization: list[OrganizationModel]


class EventUserModel(CamelModel):
    """Pydantic модель связи пользователя с событием.

    Представляет отношение участия пользователя в событии.
    Использует camelCase для совместимости с API.
    """

    user: UserModel
    event: EventModel
