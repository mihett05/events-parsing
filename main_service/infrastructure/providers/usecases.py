from dishka import Provider, provide_all, Scope

from application.events.usecases import (
    CreateEventUseCase,
    DeleteEventUseCase,
    MakeRepeatableEventTypeUseCase,
    MakeSingleEventTypeUseCase,
    ReadEventUseCase,
    ReadOrganizationEventsUseCase,
    ReadUserEventsUseCase,
    UpdateEventUseCase,
)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    events = provide_all(
        CreateEventUseCase,
        DeleteEventUseCase,
        MakeRepeatableEventTypeUseCase,
        MakeSingleEventTypeUseCase,
        ReadEventUseCase,
        ReadOrganizationEventsUseCase,
        ReadUserEventsUseCase,
        UpdateEventUseCase,
    )
