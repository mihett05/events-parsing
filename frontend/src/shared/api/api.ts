import { baseApi as api } from './base';
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    createAttachmentsV1AttachmentsEventIdPost: build.mutation<
      CreateAttachmentsV1AttachmentsEventIdPostApiResponse,
      CreateAttachmentsV1AttachmentsEventIdPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/attachments/${queryArg.eventId}`,
        method: 'POST',
        body: queryArg.bodyCreateAttachmentsV1AttachmentsEventIdPost,
      }),
    }),
    readUserV1AttachmentsAttachmentIdGet: build.query<
      ReadUserV1AttachmentsAttachmentIdGetApiResponse,
      ReadUserV1AttachmentsAttachmentIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/attachments/${queryArg.attachmentId}` }),
    }),
    loginUserV1AuthLoginPost: build.mutation<
      LoginUserV1AuthLoginPostApiResponse,
      LoginUserV1AuthLoginPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/auth/login`,
        method: 'POST',
        body: queryArg.authenticateUserModelDto,
      }),
    }),
    registerUserV1AuthRegisterPost: build.mutation<
      RegisterUserV1AuthRegisterPostApiResponse,
      RegisterUserV1AuthRegisterPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/auth/register`,
        method: 'POST',
        body: queryArg.createUserModelDto,
      }),
    }),
    refreshTokenV1AuthRefreshPost: build.mutation<
      RefreshTokenV1AuthRefreshPostApiResponse,
      RefreshTokenV1AuthRefreshPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/auth/refresh`,
        method: 'POST',
        cookies: {
          refresh: queryArg.refresh,
        },
      }),
    }),
    readAllEventsV1EventsCalendarGet: build.query<
      ReadAllEventsV1EventsCalendarGetApiResponse,
      ReadAllEventsV1EventsCalendarGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/calendar`,
        params: {
          start_date: queryArg.startDate,
          end_date: queryArg.endDate,
        },
      }),
    }),
    readAllEventsV1EventsFeedGet: build.query<
      ReadAllEventsV1EventsFeedGetApiResponse,
      ReadAllEventsV1EventsFeedGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/feed`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
          start_date: queryArg.startDate,
          end_date: queryArg.endDate,
          organization_id: queryArg.organizationId,
          type_: queryArg['type'],
          format_: queryArg.format,
        },
      }),
    }),
    getTypesAndFormatsV1EventsFeedFiltersGet: build.query<
      GetTypesAndFormatsV1EventsFeedFiltersGetApiResponse,
      GetTypesAndFormatsV1EventsFeedFiltersGetApiArg
    >({
      query: () => ({ url: `/v1/events/feed_filters` }),
    }),
    createEventV1EventsPost: build.mutation<
      CreateEventV1EventsPostApiResponse,
      CreateEventV1EventsPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/`,
        method: 'POST',
        body: queryArg.createEventModelDto,
      }),
    }),
    readEventV1EventsEventIdGet: build.query<
      ReadEventV1EventsEventIdGetApiResponse,
      ReadEventV1EventsEventIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/events/${queryArg.eventId}` }),
    }),
    updateEventV1EventsEventIdPut: build.mutation<
      UpdateEventV1EventsEventIdPutApiResponse,
      UpdateEventV1EventsEventIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/${queryArg.eventId}`,
        method: 'PUT',
        body: queryArg.updateEventModelDto,
      }),
    }),
    deleteEventV1EventsEventIdDelete: build.mutation<
      DeleteEventV1EventsEventIdDeleteApiResponse,
      DeleteEventV1EventsEventIdDeleteApiArg
    >({
      query: (queryArg) => ({ url: `/v1/events/${queryArg.eventId}`, method: 'DELETE' }),
    }),
    readAllUsersV1UsersGet: build.query<
      ReadAllUsersV1UsersGetApiResponse,
      ReadAllUsersV1UsersGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
        },
      }),
    }),
    deleteUserV1UsersDelete: build.mutation<
      DeleteUserV1UsersDeleteApiResponse,
      DeleteUserV1UsersDeleteApiArg
    >({
      query: () => ({ url: `/v1/users/`, method: 'DELETE' }),
    }),
    getMeV1UsersMeGet: build.query<GetMeV1UsersMeGetApiResponse, GetMeV1UsersMeGetApiArg>({
      query: () => ({ url: `/v1/users/me` }),
    }),
    readUserV1UsersUserIdGet: build.query<
      ReadUserV1UsersUserIdGetApiResponse,
      ReadUserV1UsersUserIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/users/${queryArg.userId}` }),
    }),
    updateUserV1UsersUserIdPut: build.mutation<
      UpdateUserV1UsersUserIdPutApiResponse,
      UpdateUserV1UsersUserIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/${queryArg.userId}`,
        method: 'PUT',
        body: queryArg.updateUserModelDto,
      }),
    }),
    createOrganizationV1OrganizationsPost: build.mutation<
      CreateOrganizationV1OrganizationsPostApiResponse,
      CreateOrganizationV1OrganizationsPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/organizations/`,
        method: 'POST',
        body: queryArg.createOrganizationModelDto,
      }),
    }),
    readAllOrganizationsV1OrganizationsGet: build.query<
      ReadAllOrganizationsV1OrganizationsGetApiResponse,
      ReadAllOrganizationsV1OrganizationsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/organizations/`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
        },
      }),
    }),
    readOrganizationV1OrganizationsOrganizationIdGet: build.query<
      ReadOrganizationV1OrganizationsOrganizationIdGetApiResponse,
      ReadOrganizationV1OrganizationsOrganizationIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/organizations/${queryArg.organizationId}` }),
    }),
    updateOrganizationV1OrganizationsOrganizationIdPut: build.mutation<
      UpdateOrganizationV1OrganizationsOrganizationIdPutApiResponse,
      UpdateOrganizationV1OrganizationsOrganizationIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/organizations/${queryArg.organizationId}`,
        method: 'PUT',
        body: queryArg.updateOrganizationModelDto,
      }),
    }),
    deleteOrganizationV1OrganizationsOrganizationIdDelete: build.mutation<
      DeleteOrganizationV1OrganizationsOrganizationIdDeleteApiResponse,
      DeleteOrganizationV1OrganizationsOrganizationIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/organizations/${queryArg.organizationId}`,
        method: 'DELETE',
      }),
    }),
    readAllNotificationsV1NotificationsGet: build.query<
      ReadAllNotificationsV1NotificationsGetApiResponse,
      ReadAllNotificationsV1NotificationsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/notifications/`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
        },
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as api };
export type CreateAttachmentsV1AttachmentsEventIdPostApiResponse =
  /** status 200 Successful Response */ AttachmentModel[];
export type CreateAttachmentsV1AttachmentsEventIdPostApiArg = {
  eventId: number;
  bodyCreateAttachmentsV1AttachmentsEventIdPost: BodyCreateAttachmentsV1AttachmentsEventIdPost;
};
export type ReadUserV1AttachmentsAttachmentIdGetApiResponse =
  /** status 200 Successful Response */ AttachmentModel;
export type ReadUserV1AttachmentsAttachmentIdGetApiArg = {
  attachmentId: string;
};
export type LoginUserV1AuthLoginPostApiResponse =
  /** status 200 Successful Response */ UserWithTokenModel;
export type LoginUserV1AuthLoginPostApiArg = {
  authenticateUserModelDto: AuthenticateUserModelDto;
};
export type RegisterUserV1AuthRegisterPostApiResponse =
  /** status 200 Successful Response */ UserWithTokenModel;
export type RegisterUserV1AuthRegisterPostApiArg = {
  createUserModelDto: CreateUserModelDto;
};
export type RefreshTokenV1AuthRefreshPostApiResponse =
  /** status 200 Successful Response */ UserWithTokenModel;
export type RefreshTokenV1AuthRefreshPostApiArg = {
  refresh: string | null;
};
export type ReadAllEventsV1EventsCalendarGetApiResponse =
  /** status 200 Successful Response */ EventModel[];
export type ReadAllEventsV1EventsCalendarGetApiArg = {
  startDate?: string | null;
  endDate?: string | null;
};
export type ReadAllEventsV1EventsFeedGetApiResponse =
  /** status 200 Successful Response */ EventModel[];
export type ReadAllEventsV1EventsFeedGetApiArg = {
  page?: number;
  pageSize?: number;
  startDate?: string | null;
  endDate?: string | null;
  organizationId?: number | null;
  type?: EventTypeEnum | null;
  format?: EventFormatEnum | null;
};
export type GetTypesAndFormatsV1EventsFeedFiltersGetApiResponse =
  /** status 200 Successful Response */ FilterModel;
export type GetTypesAndFormatsV1EventsFeedFiltersGetApiArg = void;
export type CreateEventV1EventsPostApiResponse = /** status 200 Successful Response */ EventModel;
export type CreateEventV1EventsPostApiArg = {
  createEventModelDto: CreateEventModelDto;
};
export type ReadEventV1EventsEventIdGetApiResponse =
  /** status 200 Successful Response */ EventModel;
export type ReadEventV1EventsEventIdGetApiArg = {
  eventId: number;
};
export type UpdateEventV1EventsEventIdPutApiResponse =
  /** status 200 Successful Response */ EventModel;
export type UpdateEventV1EventsEventIdPutApiArg = {
  eventId: number;
  updateEventModelDto: UpdateEventModelDto;
};
export type DeleteEventV1EventsEventIdDeleteApiResponse =
  /** status 200 Successful Response */ EventModel;
export type DeleteEventV1EventsEventIdDeleteApiArg = {
  eventId: number;
};
export type ReadAllUsersV1UsersGetApiResponse = /** status 200 Successful Response */ UserModel[];
export type ReadAllUsersV1UsersGetApiArg = {
  page?: number;
  pageSize?: number;
};
export type DeleteUserV1UsersDeleteApiResponse = /** status 200 Successful Response */ UserModel;
export type DeleteUserV1UsersDeleteApiArg = void;
export type GetMeV1UsersMeGetApiResponse = /** status 200 Successful Response */ UserModel;
export type GetMeV1UsersMeGetApiArg = void;
export type ReadUserV1UsersUserIdGetApiResponse = /** status 200 Successful Response */ UserModel;
export type ReadUserV1UsersUserIdGetApiArg = {
  userId: number;
};
export type UpdateUserV1UsersUserIdPutApiResponse = /** status 200 Successful Response */ UserModel;
export type UpdateUserV1UsersUserIdPutApiArg = {
  userId: number;
  updateUserModelDto: UpdateUserModelDto;
};
export type CreateOrganizationV1OrganizationsPostApiResponse =
  /** status 200 Successful Response */ OrganizationModel;
export type CreateOrganizationV1OrganizationsPostApiArg = {
  createOrganizationModelDto: CreateOrganizationModelDto;
};
export type ReadAllOrganizationsV1OrganizationsGetApiResponse =
  /** status 200 Successful Response */ OrganizationModel[];
export type ReadAllOrganizationsV1OrganizationsGetApiArg = {
  page?: number | null;
  pageSize?: number | null;
};
export type ReadOrganizationV1OrganizationsOrganizationIdGetApiResponse =
  /** status 200 Successful Response */ OrganizationModel;
export type ReadOrganizationV1OrganizationsOrganizationIdGetApiArg = {
  organizationId: number;
};
export type UpdateOrganizationV1OrganizationsOrganizationIdPutApiResponse =
  /** status 200 Successful Response */ OrganizationModel;
export type UpdateOrganizationV1OrganizationsOrganizationIdPutApiArg = {
  organizationId: number;
  updateOrganizationModelDto: UpdateOrganizationModelDto;
};
export type DeleteOrganizationV1OrganizationsOrganizationIdDeleteApiResponse =
  /** status 200 Successful Response */ OrganizationModel;
export type DeleteOrganizationV1OrganizationsOrganizationIdDeleteApiArg = {
  organizationId: number;
};
export type ReadAllNotificationsV1NotificationsGetApiResponse =
  /** status 200 Successful Response */ NotificationModel[];
export type ReadAllNotificationsV1NotificationsGetApiArg = {
  page?: number;
  pageSize?: number;
};
export type AttachmentModel = {
  id: string;
  filename: string;
  extension: string;
  createdAt: string;
  fileLink: string;
  mailId?: number | null;
  eventId?: number | null;
};
export type ErrorModel = {
  message: string;
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type BodyCreateAttachmentsV1AttachmentsEventIdPost = {
  files: Blob[];
};
export type UserModel = {
  id: number;
  email: string;
  fullname: string;
  isActive: boolean;
  telegramId: number | null;
  createdAt: string;
};
export type UserWithTokenModel = {
  accessToken: string;
  user: UserModel;
};
export type AuthenticateUserModelDto = {
  email: string;
  password: string;
};
export type CreateUserModelDto = {
  email: string;
  password: string;
  fullname?: string;
  isActive?: boolean;
};
export type EventTypeEnum =
  | '\u0425\u0430\u043A\u0430\u0442\u043E\u043D'
  | '\u041A\u043E\u043D\u0444\u0435\u0440\u0435\u043D\u0446\u0438\u044F'
  | '\u041A\u043E\u043D\u0442\u0435\u0441\u0442'
  | '\u0414\u0440\u0443\u0433\u043E\u0435';
export type EventFormatEnum =
  | '\u0414\u0438\u0441\u0442\u0430\u043D\u0446\u0438\u043E\u043D\u043D\u043E'
  | '\u041E\u0447\u043D\u043E'
  | '\u0421\u043C\u0435\u0448\u0430\u043D\u043D\u043E\u0435'
  | '\u0414\u0440\u0443\u0433\u043E\u0435';
export type EventModel = {
  id: number;
  title: string;
  type: EventTypeEnum;
  format: EventFormatEnum;
  createdAt: string;
  isVisible: boolean;
  location: string | null;
  description: string | null;
  startDate: string;
  endDate: string | null;
  endRegistration?: string | null;
  organizationId?: number | null;
};
export type OrganizationModel = {
  title: string;
  createdAt: string;
  id: number;
  ownerId: number;
};
export type FilterModel = {
  type: EventTypeEnum[];
  format: EventFormatEnum[];
  organization: OrganizationModel[];
};
export type CreateEventModelDto = {
  title: string;
  type: EventTypeEnum;
  format: EventFormatEnum;
  location: string | null;
  description: string | null;
  endDate: string;
  startDate: string;
  endRegistration: string;
  organizationId: number;
};
export type UpdateEventModelDto = {
  title: string;
  description: string;
};
export type UpdateUserModelDto = {
  fullname: string;
  telegramId?: number | null;
};
export type CreateOrganizationModelDto = {
  title: string;
  createdAt: string;
};
export type UpdateOrganizationModelDto = {
  title: string;
};
export type NotificationTypeEnum = 'EMAIL' | 'TELEGRAM';
export type NotificationFormatEnum = 'HTML' | 'RAW_TEXT';
export type NotificationStatusEnum = 'SENT' | 'UNSENT';
export type NotificationModel = {
  id: number;
  createdAt: string;
  recipientId: number;
  text: string;
  type: NotificationTypeEnum;
  format: NotificationFormatEnum;
  status: NotificationStatusEnum;
};
export const {
  useCreateAttachmentsV1AttachmentsEventIdPostMutation,
  useReadUserV1AttachmentsAttachmentIdGetQuery,
  useLoginUserV1AuthLoginPostMutation,
  useRegisterUserV1AuthRegisterPostMutation,
  useRefreshTokenV1AuthRefreshPostMutation,
  useReadAllEventsV1EventsCalendarGetQuery,
  useReadAllEventsV1EventsFeedGetQuery,
  useGetTypesAndFormatsV1EventsFeedFiltersGetQuery,
  useCreateEventV1EventsPostMutation,
  useReadEventV1EventsEventIdGetQuery,
  useUpdateEventV1EventsEventIdPutMutation,
  useDeleteEventV1EventsEventIdDeleteMutation,
  useReadAllUsersV1UsersGetQuery,
  useDeleteUserV1UsersDeleteMutation,
  useGetMeV1UsersMeGetQuery,
  useReadUserV1UsersUserIdGetQuery,
  useUpdateUserV1UsersUserIdPutMutation,
  useCreateOrganizationV1OrganizationsPostMutation,
  useReadAllOrganizationsV1OrganizationsGetQuery,
  useReadOrganizationV1OrganizationsOrganizationIdGetQuery,
  useUpdateOrganizationV1OrganizationsOrganizationIdPutMutation,
  useDeleteOrganizationV1OrganizationsOrganizationIdDeleteMutation,
  useReadAllNotificationsV1NotificationsGetQuery,
} = injectedRtkApi;
