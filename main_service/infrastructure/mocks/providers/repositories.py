from dishka import Provider, Scope, provide
from domain.attachments.repositories import AttachmentsRepository
from domain.events.repositories import EventsRepository
from domain.mails.repositories import MailsRepository
from domain.notifications.repositories import NotificationsRepository
from domain.organizations.repositories import (
    OrganizationsRepository,
    OrganizationTokensRepository,
)
from domain.users.repositories import (
    UsersRepository,
)

from infrastructure.mocks.repositories.attachments import (
    AttachmentsMemoryRepository,
)
from infrastructure.mocks.repositories.events import EventsMemoryRepository
from infrastructure.mocks.repositories.mails import MailsMemoryRepository
from infrastructure.mocks.repositories.notifications import (
    NotificationsMemoryRepository,
)
from infrastructure.mocks.repositories.ogranizations.repositories import (
    OrganizationsMemoryRepository,
    OrganizationTokensMemoryRepository,
)
from infrastructure.mocks.repositories.users import (
    UsersMemoryRepository,
)


class RepositoriesProvider(Provider):
    scope = Scope.APP

    mails = provide(source=MailsMemoryRepository, provides=MailsRepository)
    events = provide(source=EventsMemoryRepository, provides=EventsRepository)
    users = provide(source=UsersMemoryRepository, provides=UsersRepository)
    notifications = provide(
        source=NotificationsMemoryRepository, provides=NotificationsRepository
    )
    organizations = provide(
        source=OrganizationsMemoryRepository, provides=OrganizationsRepository
    )
    attachments = provide(
        source=AttachmentsMemoryRepository,
        provides=AttachmentsRepository,
    )
    organization_tokens = provide(
        source=OrganizationTokensMemoryRepository,
        provides=OrganizationTokensRepository,
    )
