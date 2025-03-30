from dishka import Provider, provide_all, Scope

from application.events.usecases import (
    CreateEventUseCase,
    DeleteEventUseCase,
    ReadEventUseCase,
    ReadOrganizationEventsUseCase,
    ReadUserEventsUseCase,
    UpdateEventUseCase, ReadAllEventUseCase,
)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    events = provide_all(
        CreateEventUseCase,
        DeleteEventUseCase,
        ReadEventUseCase,
        ReadOrganizationEventsUseCase,
        ReadUserEventsUseCase,
        ReadAllEventUseCase,
        UpdateEventUseCase,
    )
