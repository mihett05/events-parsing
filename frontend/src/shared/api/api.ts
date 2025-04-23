import { baseApi as api } from './base';
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
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
    readAllEventsV1EventsGet: build.query<
      ReadAllEventsV1EventsGetApiResponse,
      ReadAllEventsV1EventsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/v1/events/`,
        params: {
          page: queryArg.page,
          page_size: queryArg.pageSize,
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
  }),
  overrideExisting: false,
});
export { injectedRtkApi as api };
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
export type ReadAllEventsV1EventsGetApiResponse =
  /** status 200 Successful Response */ EventModel[];
export type ReadAllEventsV1EventsGetApiArg = {
  page?: number;
  pageSize?: number;
};
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
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
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
export type EventModel = {
  id: number;
  title: string;
  type: string;
  format: string;
  createdAt: string;
  isVisible: boolean;
  location: string | null;
  description: string | null;
  startDate: string;
  endDate: string | null;
  endRegistration?: string | null;
};
export type ErrorModel = {
  message: string;
};
export type CreateEventModelDto = {
  title: string;
  type: string;
  format: string;
  location: string | null;
  description: string | null;
  endDate: string;
  startDate: string;
  endRegistration: string;
};
export type UpdateEventModelDto = {
  title: string;
  description: string;
};
export type UpdateUserModelDto = {
  fullname: string;
  telegramId?: number | null;
};
export const {
  useLoginUserV1AuthLoginPostMutation,
  useRegisterUserV1AuthRegisterPostMutation,
  useRefreshTokenV1AuthRefreshPostMutation,
  useReadAllEventsV1EventsGetQuery,
  useCreateEventV1EventsPostMutation,
  useReadEventV1EventsEventIdGetQuery,
  useUpdateEventV1EventsEventIdPutMutation,
  useDeleteEventV1EventsEventIdDeleteMutation,
  useReadAllUsersV1UsersGetQuery,
  useDeleteUserV1UsersDeleteMutation,
  useGetMeV1UsersMeGetQuery,
  useReadUserV1UsersUserIdGetQuery,
  useUpdateUserV1UsersUserIdPutMutation,
} = injectedRtkApi;
