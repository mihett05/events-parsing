from application.notifications.factory import NotificationGatewayAbstractFactory
from dishka import Provider, Scope, provide
from domain.attachments.repositories import AttachmentsRepository
from domain.events.repositories import EventsRepository, EventUsersRepository
from domain.mails.repositories import MailsRepository
from domain.notifications.repositories import NotificationsRepository
from domain.organizations.repositories import (
    OrganizationsRepository,
    OrganizationTokensRepository,
)
from domain.users.repositories import (
    TelegramTokensRepository,
    UserActivationTokenRepository,
    UserOrganizationRolesRepository,
    UsersRepository,
)

from infrastructure.gateways.notifications.factory import (
    NotificationGatewayFactory,
)
from infrastructure.gateways.notifications.gateways import (
    NotificationTelegramGateway,
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
    TelegramTokensMemoryRepository,
    UserActivationTokenMemoryRepository,
    UserOrganizationsRolesMemoryRepository,
    UsersMemoryRepository,
)


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST
    mails = provide(source=MailsMemoryRepository, provides=MailsRepository)
    events = provide(source=EventsMemoryRepository, provides=EventsRepository)
    event_users = provide(source=EventUsersRepository, provides=EventUsersRepository)
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
    user_organization_roles = provide(
        source=UserOrganizationsRolesMemoryRepository,
        provides=UserOrganizationRolesRepository,
    )
    organization_tokens = provide(
        source=OrganizationTokensMemoryRepository,
        provides=OrganizationTokensRepository,
    )
    telegram_tokens = provide(
        source=TelegramTokensMemoryRepository, provides=TelegramTokensRepository
    )
    roles = provide(
        source=UserOrganizationsRolesMemoryRepository,
        provides=UserOrganizationRolesRepository,
    )
    activation_token_repository = provide(
        source=UserActivationTokenMemoryRepository,
        provides=UserActivationTokenRepository,
    )
