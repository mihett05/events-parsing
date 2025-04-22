from dishka import Provider, Scope, provide
from domain.events.repositories import EventsRepository
from domain.mails.repositories import MailsRepository

from infrastructure.mocks.repositories.events import EventsMemoryRepository
from infrastructure.mocks.repositories.mails import MailsMemoryRepository


class RepositoriesProvider(Provider):
    scope = Scope.APP

    mails = provide(source=MailsMemoryRepository, provides=MailsRepository)
    events = provide(source=EventsMemoryRepository, provides=EventsRepository)
