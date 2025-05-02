import application.attachments.usecases as attachments_use_cases
import application.auth.usecases as auth_use_cases
import application.events.usecases as event_use_cases
import application.mails.usecases as mails_use_cases
import application.notifications.usecases as notification_use_cases
import application.organizations.usecases as organizations_use_cases
import application.users.usecases as users_use_cases
from dishka import Provider, Scope, provide_all


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    events = provide_all(
        event_use_cases.CreateEventUseCase,
        event_use_cases.DeduplicateEventUseCase,
        event_use_cases.DeleteEventUseCase,
        event_use_cases.FindEventUseCase,
        event_use_cases.ReadEventUseCase,
        event_use_cases.ReadForFeedEventsUseCase,
        event_use_cases.ReadOrganizationEventsUseCase,
        event_use_cases.ReadUserEventsUseCase,
        event_use_cases.ReadAllEventUseCase,
        event_use_cases.ParseEventsUseCase,
        event_use_cases.UpdateEventUseCase,
    )

    organizations = provide_all(
        organizations_use_cases.CreateOrganizationUseCase,
        organizations_use_cases.ReadOrganizationUseCase,
        organizations_use_cases.UpdateOrganizationUseCase,
        organizations_use_cases.DeleteOrganizationUseCase,
        organizations_use_cases.ReadAllOrganizationUseCase,
    )

    mails = provide_all(
        mails_use_cases.ReadMailUseCase,
        mails_use_cases.ReadUnprocessedMailUseCase,
        mails_use_cases.UpdateMailUseCase,
        mails_use_cases.CreateMailsUseCase,
    )

    users = provide_all(
        users_use_cases.ReadUserUseCase,
        users_use_cases.UpdateUserUseCase,
        users_use_cases.DeleteUserUseCase,
        users_use_cases.ReadAllUsersUseCase,
        users_use_cases.ReadUsersByIdsUseCase,
        users_use_cases.CreateUserUseCase,
    )

    auth = provide_all(
        auth_use_cases.RegisterUseCase,
        auth_use_cases.LoginUseCase,
        auth_use_cases.AuthenticateUseCase,
        auth_use_cases.AuthorizeUseCase,
        auth_use_cases.CreateTokenPairUseCase,
    )

    notifications = provide_all(
        notification_use_cases.CreateNotificationUseCase,
        notification_use_cases.ReadNotificationUseCase,
        notification_use_cases.ReadAllNotificationsUseCase,
        notification_use_cases.UpdateManyNotificationUseCase,
        notification_use_cases.DeleteNotificationUseCase,
    )

    attachments = provide_all(
        attachments_use_cases.CreateAttachmentUseCase,
        attachments_use_cases.ReadAttachmentUseCase,
        attachments_use_cases.DeleteAttachmentUseCase,
    )
