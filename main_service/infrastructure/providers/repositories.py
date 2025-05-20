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

from infrastructure.database.repositories import (
    AttachmentsDatabaseRepository,
    EventsDatabaseRepository,
    MailsDatabaseRepository,
    NotificationsDatabaseRepository,
    UserActivationTokenDatabaseRepository,
    UserOrganizationRolesDatabaseRepository,
    UsersDatabaseRepository,
)
from infrastructure.database.repositories.events import (
    EventsUserDatabaseRepository,
)
from infrastructure.database.repositories.organizations import (
    OrganizationsDatabaseRepository,
    OrganizationTokensDatabaseRepository,
)
from infrastructure.database.repositories.users import (
    TelegramTokensDatabaseRepository,
    UserOrganizationRolesDatabaseRepository,
    UsersDatabaseRepository,
)


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST
    attachments_repository = provide(
        source=AttachmentsDatabaseRepository, provides=AttachmentsRepository
    )
    events_repository = provide(
        source=EventsDatabaseRepository, provides=EventsRepository
    )
    event_users_repository = provide(
        source=EventsUserDatabaseRepository, provides=EventUsersRepository
    )
    mails_repository = provide(source=MailsDatabaseRepository, provides=MailsRepository)
    organizations_repository = provide(
        source=OrganizationsDatabaseRepository, provides=OrganizationsRepository
    )
    organization_tokens_repository = provide(
        source=OrganizationTokensDatabaseRepository,
        provides=OrganizationTokensRepository,
    )
    users_repository = provide(source=UsersDatabaseRepository, provides=UsersRepository)
    notification_repository = provide(
        source=NotificationsDatabaseRepository, provides=NotificationsRepository
    )
    user_organization_roles_repository = provide(
        source=UserOrganizationRolesDatabaseRepository,
        provides=UserOrganizationRolesRepository,
    )
    telegram_tokens = provide(
        source=TelegramTokensDatabaseRepository,
        provides=TelegramTokensRepository,
    )
    activation_token_repository = provide(
        source=UserActivationTokenDatabaseRepository,
        provides=UserActivationTokenRepository,
    )
