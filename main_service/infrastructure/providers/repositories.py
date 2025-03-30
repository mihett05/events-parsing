from dishka import Provider, Scope, provide

from domain.events.repositories import EventsRepository
from infrastructure.database.repositories.events import EventsDbRepository


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    events_repository = provide(
        source=EventsDbRepository, provides=EventsRepository
    )
