from dishka import Provider, Scope, provide

from domain.events.repositories import EventsRepository
from domain.mails.repositories import MailsRepository
from infrastructure.database.repositories.events import EventsDatabaseRepository
from infrastructure.database.repositories.mails import MailsDatabaseRepository



class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    events_repository = provide(
        source=EventsDatabaseRepository, provides=EventsRepository
    )
    mails_repository = provide(
        source=MailsDatabaseRepository, provides=MailsRepository
    )
