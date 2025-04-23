from dishka import Provider, Scope, provide
from domain.events.repositories import EventsRepository
from domain.mails.repositories import MailsRepository
from domain.users.repositories import UsersRepository
from domain.notifications.repositories import NotificationRepository

from infrastructure.mocks.repositories.events import EventsMemoryRepository
from infrastructure.mocks.repositories.mails import MailsMemoryRepository
from infrastructure.mocks.repositories.users import (
    UsersMemoryRepository,
)
from infrastructure.mocks.repositories.notifications import (
    NotificationMemoryRepository,
)


class RepositoriesProvider(Provider):
    scope = Scope.APP

    mails = provide(source=MailsMemoryRepository, provides=MailsRepository)
    events = provide(source=EventsMemoryRepository, provides=EventsRepository)
    users = provide(source=UsersMemoryRepository, provides=UsersRepository)
    notifications = provide(
        source=NotificationMemoryRepository, provides=NotificationRepository
    )
