from dishka import Provider, Scope, provide

from domain.attachments.repositories import AttachmentsRepository
from domain.events.repositories import EventsRepository
from domain.mails.repositories import MailsRepository
from domain.users.repositories import UsersRepository
from infrastructure.mocks.repositories.attachments import (
    AttachmentsMemoryRepository,
)
from infrastructure.mocks.repositories.events import EventsMemoryRepository
from infrastructure.mocks.repositories.mails import MailsMemoryRepository
from infrastructure.mocks.repositories.users import (
    UsersMemoryRepository,
)


class RepositoriesProvider(Provider):
    scope = Scope.APP

    mails = provide(source=MailsMemoryRepository, provides=MailsRepository)
    events = provide(source=EventsMemoryRepository, provides=EventsRepository)
    users = provide(source=UsersMemoryRepository, provides=UsersRepository)
    attachments = provide(
        source=AttachmentsMemoryRepository,
        provides=AttachmentsRepository,
    )
