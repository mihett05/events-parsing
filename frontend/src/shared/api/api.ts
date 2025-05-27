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
    readAttachmentV1AttachmentsAttachmentIdGet: build.query<
      ReadAttachmentV1AttachmentsAttachmentIdGetApiResponse,
      ReadAttachmentV1AttachmentsAttachmentIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/attachments/${queryArg.attachmentId}` }),
    }),
    deleteAttachmentV1AttachmentsAttachmentIdDelete: build.mutation<
      DeleteAttachmentV1AttachmentsAttachmentIdDeleteApiResponse,
      DeleteAttachmentV1AttachmentsAttachmentIdDeleteApiArg
    >({
      query: (queryArg) => ({ url: `/v1/attachments/${queryArg.attachmentId}`, method: 'DELETE' }),
    }),
    updateAttachmentV1AttachmentsAttachmentIdPut: build.mutation<
      UpdateAttachmentV1AttachmentsAttachmentIdPutApiResponse,
      UpdateAttachmentV1AttachmentsAttachmentIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/attachments/${queryArg.attachmentId}`,
        method: 'PUT',
        body: queryArg.updateAttachmentModelDto,
      }),
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
    validateTokenV1AuthActivateTokenUuidGet: build.query<
      ValidateTokenV1AuthActivateTokenUuidGetApiResponse,
      ValidateTokenV1AuthActivateTokenUuidGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/auth/activate/${queryArg.tokenUuid}` }),
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
    readAllEventsV1EventsGet: build.query<
      ReadAllEventsV1EventsGetApiResponse,
      ReadAllEventsV1EventsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
          organization_id: queryArg.organizationId,
          type: queryArg['type'],
          format: queryArg.format,
          end_date: queryArg.endDate,
          start_date: queryArg.startDate,
        },
      }),
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
    getFilterValuesV1EventsFiltersGet: build.query<
      GetFilterValuesV1EventsFiltersGetApiResponse,
      GetFilterValuesV1EventsFiltersGetApiArg
    >({
      query: () => ({ url: `/v1/events/filters` }),
    }),
    createIcalV1EventsSubscribeIcalPost: build.mutation<
      CreateIcalV1EventsSubscribeIcalPostApiResponse,
      CreateIcalV1EventsSubscribeIcalPostApiArg
    >({
      query: () => ({ url: `/v1/events/subscribe/ical`, method: 'POST' }),
    }),
    deleteIcalV1EventsSubscribeIcalDelete: build.mutation<
      DeleteIcalV1EventsSubscribeIcalDeleteApiResponse,
      DeleteIcalV1EventsSubscribeIcalDeleteApiArg
    >({
      query: () => ({ url: `/v1/events/subscribe/ical`, method: 'DELETE' }),
    }),
    readIcalV1EventsSubscribeIcalUuidGet: build.query<
      ReadIcalV1EventsSubscribeIcalUuidGetApiResponse,
      ReadIcalV1EventsSubscribeIcalUuidGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/events/subscribe/ical/${queryArg.uuid}` }),
    }),
    readForUserV1EventsSubscribeMyGet: build.query<
      ReadForUserV1EventsSubscribeMyGetApiResponse,
      ReadForUserV1EventsSubscribeMyGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/subscribe/my`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
        },
      }),
    }),
    readSubscribersV1EventsSubscribeEventIdGet: build.query<
      ReadSubscribersV1EventsSubscribeEventIdGetApiResponse,
      ReadSubscribersV1EventsSubscribeEventIdGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/subscribe/${queryArg.eventId}`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
        },
      }),
    }),
    subscribeV1EventsSubscribeEventIdPost: build.mutation<
      SubscribeV1EventsSubscribeEventIdPostApiResponse,
      SubscribeV1EventsSubscribeEventIdPostApiArg
    >({
      query: (queryArg) => ({ url: `/v1/events/subscribe/${queryArg.eventId}`, method: 'POST' }),
    }),
    unsubscribeV1EventsSubscribeEventIdDelete: build.mutation<
      UnsubscribeV1EventsSubscribeEventIdDeleteApiResponse,
      UnsubscribeV1EventsSubscribeEventIdDeleteApiArg
    >({
      query: (queryArg) => ({ url: `/v1/events/subscribe/${queryArg.eventId}`, method: 'DELETE' }),
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
    updateUserV1UsersMePut: build.mutation<
      UpdateUserV1UsersMePutApiResponse,
      UpdateUserV1UsersMePutApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/me`,
        method: 'PUT',
        body: queryArg.updateUserModelDto,
      }),
    }),
    readUserV1UsersUserIdGet: build.query<
      ReadUserV1UsersUserIdGetApiResponse,
      ReadUserV1UsersUserIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/users/${queryArg.userId}` }),
    }),
    createTelegramLinkV1UsersTelegramPost: build.mutation<
      CreateTelegramLinkV1UsersTelegramPostApiResponse,
      CreateTelegramLinkV1UsersTelegramPostApiArg
    >({
      query: () => ({ url: `/v1/users/telegram`, method: 'POST' }),
    }),
    readUserRoleV1UsersRolesUserIdOrganizationIdGet: build.query<
      ReadUserRoleV1UsersRolesUserIdOrganizationIdGetApiResponse,
      ReadUserRoleV1UsersRolesUserIdOrganizationIdGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/roles/${queryArg.userId}/${queryArg.organizationId}`,
      }),
    }),
    deleteUserRoleV1UsersRolesUserIdOrganizationIdDelete: build.mutation<
      DeleteUserRoleV1UsersRolesUserIdOrganizationIdDeleteApiResponse,
      DeleteUserRoleV1UsersRolesUserIdOrganizationIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/roles/${queryArg.userId}/${queryArg.organizationId}`,
        method: 'DELETE',
      }),
    }),
    readUserRolesV1UsersRolesUserIdGet: build.query<
      ReadUserRolesV1UsersRolesUserIdGetApiResponse,
      ReadUserRolesV1UsersRolesUserIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/users/roles/${queryArg.userId}` }),
    }),
    createUserRoleV1UsersRolesPost: build.mutation<
      CreateUserRoleV1UsersRolesPostApiResponse,
      CreateUserRoleV1UsersRolesPostApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/roles`,
        method: 'POST',
        body: queryArg.createUserRoleModelDto,
      }),
    }),
    updateUserRoleV1UsersRolesUpdatePut: build.mutation<
      UpdateUserRoleV1UsersRolesUpdatePutApiResponse,
      UpdateUserRoleV1UsersRolesUpdatePutApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/users/roles/update`,
        method: 'PUT',
        body: queryArg.updateUserRoleModelDto,
      }),
    }),
    createTokenV1OrganizationsTokenPost: build.mutation<
      CreateTokenV1OrganizationsTokenPostApiResponse,
      CreateTokenV1OrganizationsTokenPostApiArg
    >({
      query: () => ({ url: `/v1/organizations/token`, method: 'POST' }),
    }),
    readAllTokensV1OrganizationsTokenGet: build.query<
      ReadAllTokensV1OrganizationsTokenGetApiResponse,
      ReadAllTokensV1OrganizationsTokenGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/organizations/token`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
        },
      }),
    }),
    readTokenV1OrganizationsTokenTokenIdGet: build.query<
      ReadTokenV1OrganizationsTokenTokenIdGetApiResponse,
      ReadTokenV1OrganizationsTokenTokenIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/v1/organizations/token/${queryArg.tokenId}` }),
    }),
    deleteTokenV1OrganizationsTokenTokenIdDelete: build.mutation<
      DeleteTokenV1OrganizationsTokenTokenIdDeleteApiResponse,
      DeleteTokenV1OrganizationsTokenTokenIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/organizations/token/${queryArg.tokenId}`,
        method: 'DELETE',
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
export type ReadAttachmentV1AttachmentsAttachmentIdGetApiResponse =
  /** status 200 Successful Response */ AttachmentModel;
export type ReadAttachmentV1AttachmentsAttachmentIdGetApiArg = {
  attachmentId: string;
};
export type DeleteAttachmentV1AttachmentsAttachmentIdDeleteApiResponse =
  /** status 200 Successful Response */ AttachmentModel;
export type DeleteAttachmentV1AttachmentsAttachmentIdDeleteApiArg = {
  attachmentId: string;
};
export type UpdateAttachmentV1AttachmentsAttachmentIdPutApiResponse =
  /** status 200 Successful Response */ AttachmentModel;
export type UpdateAttachmentV1AttachmentsAttachmentIdPutApiArg = {
  attachmentId: string;
  updateAttachmentModelDto: UpdateAttachmentModelDto;
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
export type ValidateTokenV1AuthActivateTokenUuidGetApiResponse =
  /** status 200 Successful Response */ any;
export type ValidateTokenV1AuthActivateTokenUuidGetApiArg = {
  tokenUuid: string;
};
export type RefreshTokenV1AuthRefreshPostApiResponse =
  /** status 200 Successful Response */ UserWithTokenModel;
export type RefreshTokenV1AuthRefreshPostApiArg = {
  refresh: string | null;
};
export type ReadAllEventsV1EventsGetApiResponse =
  /** status 200 Successful Response */ EventModel[];
export type ReadAllEventsV1EventsGetApiArg = {
  page?: number;
  pageSize?: number;
  organizationId?: number | null;
  type?: EventTypeEnum | null;
  format?: EventFormatEnum | null;
  endDate?: string | null;
  startDate?: string | null;
};
export type CreateEventV1EventsPostApiResponse = /** status 200 Successful Response */ EventModel;
export type CreateEventV1EventsPostApiArg = {
  createEventModelDto: CreateEventModelDto;
};
export type GetFilterValuesV1EventsFiltersGetApiResponse =
  /** status 200 Successful Response */ FilterModel;
export type GetFilterValuesV1EventsFiltersGetApiArg = void;
export type CreateIcalV1EventsSubscribeIcalPostApiResponse =
  /** status 200 Successful Response */ any;
export type CreateIcalV1EventsSubscribeIcalPostApiArg = void;
export type DeleteIcalV1EventsSubscribeIcalDeleteApiResponse =
  /** status 200 Successful Response */ any;
export type DeleteIcalV1EventsSubscribeIcalDeleteApiArg = void;
export type ReadIcalV1EventsSubscribeIcalUuidGetApiResponse =
  /** status 200 Successful Response */ any;
export type ReadIcalV1EventsSubscribeIcalUuidGetApiArg = {
  uuid: string;
};
export type ReadForUserV1EventsSubscribeMyGetApiResponse =
  /** status 200 Successful Response */ EventModel[];
export type ReadForUserV1EventsSubscribeMyGetApiArg = {
  page?: number;
  pageSize?: number;
};
export type ReadSubscribersV1EventsSubscribeEventIdGetApiResponse =
  /** status 200 Successful Response */ UserModel[];
export type ReadSubscribersV1EventsSubscribeEventIdGetApiArg = {
  eventId: number;
  page?: number;
  pageSize?: number;
};
export type SubscribeV1EventsSubscribeEventIdPostApiResponse =
  /** status 200 Successful Response */ EventUserModel;
export type SubscribeV1EventsSubscribeEventIdPostApiArg = {
  eventId: number;
};
export type UnsubscribeV1EventsSubscribeEventIdDeleteApiResponse =
  /** status 200 Successful Response */ EventUserModel;
export type UnsubscribeV1EventsSubscribeEventIdDeleteApiArg = {
  eventId: number;
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
export type UpdateUserV1UsersMePutApiResponse = /** status 200 Successful Response */ UserModel;
export type UpdateUserV1UsersMePutApiArg = {
  updateUserModelDto: UpdateUserModelDto;
};
export type ReadUserV1UsersUserIdGetApiResponse = /** status 200 Successful Response */ UserModel;
export type ReadUserV1UsersUserIdGetApiArg = {
  userId: number;
};
export type CreateTelegramLinkV1UsersTelegramPostApiResponse =
  /** status 200 Successful Response */ any;
export type CreateTelegramLinkV1UsersTelegramPostApiArg = void;
export type ReadUserRoleV1UsersRolesUserIdOrganizationIdGetApiResponse =
  /** status 200 Successful Response */ UserRoleModel;
export type ReadUserRoleV1UsersRolesUserIdOrganizationIdGetApiArg = {
  userId: number;
  organizationId: number;
};
export type DeleteUserRoleV1UsersRolesUserIdOrganizationIdDeleteApiResponse =
  /** status 200 Successful Response */ UserRoleModel;
export type DeleteUserRoleV1UsersRolesUserIdOrganizationIdDeleteApiArg = {
  userId: number;
  organizationId: number;
};
export type ReadUserRolesV1UsersRolesUserIdGetApiResponse =
  /** status 200 Successful Response */ UserRoleModel[];
export type ReadUserRolesV1UsersRolesUserIdGetApiArg = {
  userId: number;
};
export type CreateUserRoleV1UsersRolesPostApiResponse =
  /** status 200 Successful Response */ UserRoleModel;
export type CreateUserRoleV1UsersRolesPostApiArg = {
  createUserRoleModelDto: CreateUserRoleModelDto;
};
export type UpdateUserRoleV1UsersRolesUpdatePutApiResponse =
  /** status 200 Successful Response */ UserRoleModel;
export type UpdateUserRoleV1UsersRolesUpdatePutApiArg = {
  updateUserRoleModelDto: UpdateUserRoleModelDto;
};
export type CreateTokenV1OrganizationsTokenPostApiResponse =
  /** status 200 Successful Response */ OrganizationTokenModel;
export type CreateTokenV1OrganizationsTokenPostApiArg = void;
export type ReadAllTokensV1OrganizationsTokenGetApiResponse =
  /** status 200 Successful Response */ OrganizationTokenModel[];
export type ReadAllTokensV1OrganizationsTokenGetApiArg = {
  page?: number;
  pageSize?: number;
};
export type ReadTokenV1OrganizationsTokenTokenIdGetApiResponse =
  /** status 200 Successful Response */ OrganizationTokenModel;
export type ReadTokenV1OrganizationsTokenTokenIdGetApiArg = {
  tokenId: string;
};
export type DeleteTokenV1OrganizationsTokenTokenIdDeleteApiResponse =
  /** status 200 Successful Response */ OrganizationTokenModel;
export type DeleteTokenV1OrganizationsTokenTokenIdDeleteApiArg = {
  tokenId: string;
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
export type UpdateAttachmentModelDto = {
  filename: string;
};
export type UserNotificationSendToEnum = 'EMAIL' | 'TELEGRAM';
export type UserSettingsModel = {
  id: number;
  userId: number;
  type: UserNotificationSendToEnum;
  calendarUuid: string | null;
};
export type UserModel = {
  id: number;
  email: string;
  fullname: string;
  isActive: boolean;
  telegramId: number | null;
  createdAt: string;
  settings: UserSettingsModel;
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
  organizationId?: number | null;
  isVisible: boolean;
  location: string | null;
  description: string | null;
  attachments: AttachmentModel[];
  members: UserModel[];
  startDate: string;
  endDate: string | null;
  endRegistration?: string | null;
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
  organizationId: number | null;
  isVisible?: boolean;
};
export type OrganizationModel = {
  id: number;
  createdAt: string;
  title: string;
  ownerId: number;
};
export type FilterModel = {
  type: EventTypeEnum[];
  format: EventFormatEnum[];
  organization: OrganizationModel[];
};
export type EventUserModel = {
  user: UserModel;
  event: EventModel;
};
export type UpdateEventModelDto = {
  title: string;
  description: string;
  isVisibleStatus: boolean;
};
export type UpdateUserModelDto = {
  fullname: string;
  telegramId?: number | null;
};
export type RoleEnum =
  | 'SUPER_USER'
  | 'SUPER_AUTOBUS'
  | 'SUPER_ADMIN'
  | 'SUPER_REDACTOR'
  | 'OWNER'
  | 'ADMIN'
  | 'REDACTOR'
  | 'PUBLIC';
export type UserRoleModel = {
  userId: number;
  organizationId: number;
  role: RoleEnum;
};
export type CreateUserRoleModelDto = {
  userId: number;
  organizationId: number;
  role: RoleEnum;
};
export type UpdateUserRoleModelDto = {
  userId: number;
  organizationId: number;
  role: RoleEnum;
};
export type OrganizationTokenModel = {
  id: string;
  createdBy: number;
  usedBy?: number | null;
  isUsed?: boolean;
};
export type CreateOrganizationModelDto = {
  title: string;
  token: string;
};
export type UpdateOrganizationModelDto = {
  title: string;
};
export const {
  useCreateAttachmentsV1AttachmentsEventIdPostMutation,
  useReadAttachmentV1AttachmentsAttachmentIdGetQuery,
  useDeleteAttachmentV1AttachmentsAttachmentIdDeleteMutation,
  useUpdateAttachmentV1AttachmentsAttachmentIdPutMutation,
  useLoginUserV1AuthLoginPostMutation,
  useRegisterUserV1AuthRegisterPostMutation,
  useValidateTokenV1AuthActivateTokenUuidGetQuery,
  useRefreshTokenV1AuthRefreshPostMutation,
  useReadAllEventsV1EventsGetQuery,
  useCreateEventV1EventsPostMutation,
  useGetFilterValuesV1EventsFiltersGetQuery,
  useCreateIcalV1EventsSubscribeIcalPostMutation,
  useDeleteIcalV1EventsSubscribeIcalDeleteMutation,
  useReadIcalV1EventsSubscribeIcalUuidGetQuery,
  useReadForUserV1EventsSubscribeMyGetQuery,
  useReadSubscribersV1EventsSubscribeEventIdGetQuery,
  useSubscribeV1EventsSubscribeEventIdPostMutation,
  useUnsubscribeV1EventsSubscribeEventIdDeleteMutation,
  useReadEventV1EventsEventIdGetQuery,
  useUpdateEventV1EventsEventIdPutMutation,
  useDeleteEventV1EventsEventIdDeleteMutation,
  useReadAllUsersV1UsersGetQuery,
  useDeleteUserV1UsersDeleteMutation,
  useGetMeV1UsersMeGetQuery,
  useUpdateUserV1UsersMePutMutation,
  useReadUserV1UsersUserIdGetQuery,
  useCreateTelegramLinkV1UsersTelegramPostMutation,
  useReadUserRoleV1UsersRolesUserIdOrganizationIdGetQuery,
  useDeleteUserRoleV1UsersRolesUserIdOrganizationIdDeleteMutation,
  useReadUserRolesV1UsersRolesUserIdGetQuery,
  useCreateUserRoleV1UsersRolesPostMutation,
  useUpdateUserRoleV1UsersRolesUpdatePutMutation,
  useCreateTokenV1OrganizationsTokenPostMutation,
  useReadAllTokensV1OrganizationsTokenGetQuery,
  useReadTokenV1OrganizationsTokenTokenIdGetQuery,
  useDeleteTokenV1OrganizationsTokenTokenIdDeleteMutation,
  useCreateOrganizationV1OrganizationsPostMutation,
  useReadAllOrganizationsV1OrganizationsGetQuery,
  useReadOrganizationV1OrganizationsOrganizationIdGetQuery,
  useUpdateOrganizationV1OrganizationsOrganizationIdPutMutation,
  useDeleteOrganizationV1OrganizationsOrganizationIdDeleteMutation,
} = injectedRtkApi;
