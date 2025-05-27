from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function
from domain.notifications.dtos import CreateNotificationDto
from domain.notifications.entities import Notification

from infrastructure.database.mappers import postgres_retort

from .models import NotificationDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    NotificationDatabaseModel,
    Notification,
)
"""Конвертирует модель базы данных уведомления в доменную сущность."""

map_to_db = retort.get_converter(
    Notification,
    NotificationDatabaseModel,
    recipe=[
        link_function(
            lambda notification: notification.id,
            P[NotificationDatabaseModel].id,
        ),
        link_function(
            lambda notification: notification.created_at,
            P[NotificationDatabaseModel].created_at,
        ),
    ],
)
"""Преобразует доменную сущность уведомления в модель базы данных.

Учитывает специальные правила маппинга для полей id и created_at.
"""


map_create_dto_to_model = retort.get_converter(
    CreateNotificationDto,
    NotificationDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[NotificationDatabaseModel].id),
        allow_unlinked_optional(P[NotificationDatabaseModel].created_at),
        link_function(
            lambda dto: dto.recipient_id,
            P[NotificationDatabaseModel].recipient_id,
        ),
    ],
)
"""Конвертирует DTO для создания уведомления в модель базы данных.

Обрабатывает опциональные поля и связывает получателя уведомления.
"""
