from dishka import Provider, Scope, provide
from domain.attachments.repositories import AttachmentsRepository
from domain.events.repositories import EventsRepository
from domain.mails.repositories import MailsRepository
from domain.notifications.repositories import NotificationsRepository
from domain.organizations.repositories import OrganizationsRepository
from domain.users.repositories import UsersRepository

from infrastructure.database.repositories import (
    AttachmentsDatabaseRepository,
    EventsDatabaseRepository,
    MailsDatabaseRepository,
)
from infrastructure.database.repositories.organizations import (
    OrganizationsDatabaseRepository,
)
from infrastructure.database.repositories.users import UsersDatabaseRepository
from infrastructure.mocks.repositories.notifications import (
    NotificationsMemoryRepository,
)


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    attachments_repository = provide(
        source=AttachmentsDatabaseRepository, provides=AttachmentsRepository
    )
    events_repository = provide(
        source=EventsDatabaseRepository, provides=EventsRepository
    )
    mails_repository = provide(
        source=MailsDatabaseRepository, provides=MailsRepository
    )
    organizations_repository = provide(
        source=OrganizationsDatabaseRepository, provides=OrganizationsRepository
    )
    users_repository = provide(
        source=UsersDatabaseRepository, provides=UsersRepository
    )
    notification_repository = provide(
        source=NotificationsMemoryRepository, provides=NotificationsRepository
    )
