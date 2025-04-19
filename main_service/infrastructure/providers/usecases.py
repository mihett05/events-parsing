from dishka import Provider, Scope, provide_all

import application.auth.usecases as auth_use_cases
import application.events.usecases as event_use_cases
import application.mails.usecases as mails_use_cases
import application.users.usecases as users_use_cases


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    events = provide_all(
        event_use_cases.CreateEventUseCase,
        event_use_cases.DeduplicateEventUseCase,
        event_use_cases.DeleteEventUseCase,
        event_use_cases.FindEventUseCase,
        event_use_cases.ReadEventUseCase,
        event_use_cases.ReadOrganizationEventsUseCase,
        event_use_cases.ReadUserEventsUseCase,
        event_use_cases.ReadAllEventUseCase,
        event_use_cases.ParseEventsUseCase,
        event_use_cases.UpdateEventUseCase,
    )

    mails = provide_all(
        mails_use_cases.CreateMailUseCase,
        mails_use_cases.ReadMailUseCase,
        mails_use_cases.ReadUnprocessedMailUseCase,
        mails_use_cases.UpdateMailUseCase,
    )

    users = provide_all(
        users_use_cases.ReadUserUseCase,
        users_use_cases.UpdateUserUseCase,
        users_use_cases.DeleteUserUseCase,
        users_use_cases.ReadAllUsersUseCase,
        users_use_cases.CreateUserUseCase,
    )

    auth = provide_all(
        auth_use_cases.RegisterUseCase,
        auth_use_cases.LoginUseCase,
        auth_use_cases.AuthenticateUseCase,
        auth_use_cases.AuthorizeUseCase,
    )
