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
        event_use_cases.ReadUserEventsUseCase,
        event_use_cases.ReadAllEventUseCase,
        event_use_cases.ParseEventsUseCase,
        event_use_cases.UpdateEventUseCase,
        event_use_cases.CreateEventUserUseCase,
        event_use_cases.ReadForEventEventUserUseCase,
        event_use_cases.ReadForUserEventUserUseCase,
        event_use_cases.DeleteEventUserUseCase,
    )

    organizations = provide_all(
        organizations_use_cases.CreateOrganizationUseCase,
        organizations_use_cases.ReadOrganizationUseCase,
        organizations_use_cases.UpdateOrganizationUseCase,
        organizations_use_cases.DeleteOrganizationUseCase,
        organizations_use_cases.ReadAllOrganizationUseCase,
        organizations_use_cases.CreateOrganizationTokenUseCase,
        organizations_use_cases.ReadOrganizationTokenUseCase,
        organizations_use_cases.UpdateOrganizationTokenUseCase,
        organizations_use_cases.DeleteOrganizationTokenUseCase,
        organizations_use_cases.ValidateOrganizationTokenUseCase,
        organizations_use_cases.ReadAllOrganizationTokensUseCase,
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
        users_use_cases.ReadUserRolesUseCase,
        users_use_cases.CreateTelegramTokenUseCase,
        users_use_cases.ReadTelegramTokenUseCase,
        users_use_cases.ConnectTelegramUseCase,
        users_use_cases.CreateUserRoleUseCase,
        users_use_cases.DeleteUserRoleUseCase,
        users_use_cases.ReadUserRoleUseCase,
        users_use_cases.UpdateUserRoleUseCase,
        users_use_cases.CreateUserActivationTokenUseCase,
        users_use_cases.ValidateActivationTokenUseCase,
    )

    auth = provide_all(
        auth_use_cases.RegisterUseCase,
        auth_use_cases.LoginUseCase,
        auth_use_cases.AuthenticateUseCase,
        auth_use_cases.AuthorizeUseCase,
        auth_use_cases.CreateTokenPairUseCase,
        auth_use_cases.CreateUserWithPasswordUseCase,
    )

    notifications = provide_all(
        notification_use_cases.CreateNotificationUseCase,
        notification_use_cases.ReadNotificationUseCase,
        notification_use_cases.ReadAllNotificationsUseCase,
        notification_use_cases.UpdateNotificationsStatusUseCase,
        notification_use_cases.DeleteNotificationUseCase,
        notification_use_cases.SendNotificationsUseCase,
        notification_use_cases.ProcessUnsentNotificationsUseCase,
    )

    attachments = provide_all(
        attachments_use_cases.CreateAttachmentUseCase,
        attachments_use_cases.ReadAttachmentUseCase,
        attachments_use_cases.DeleteAttachmentUseCase,
        attachments_use_cases.UpdateAttachmentUseCase,
    )
