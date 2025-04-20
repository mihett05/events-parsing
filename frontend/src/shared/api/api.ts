import { baseApi as api } from './base';
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
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
  }),
  overrideExisting: false,
});
export { injectedRtkApi as api };
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
export type EventModel = {
  title: string;
  createdAt: string;
  startDate: string;
  id: number;
  isVisible: boolean;
  description: string | null;
  endDate: string | null;
  endRegistration?: string | null;
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type ErrorModel = {
  message: string;
};
export type CreateEventModelDto = {
  title: string;
  type: string;
  format: string;
  description: string;
  organizationId: number;
  endDate: string;
  startDate: string;
  endRegistration: string;
};
export type UpdateEventModelDto = {
  title: string;
  description: string;
};
export const {
  useReadAllEventsV1EventsGetQuery,
  useCreateEventV1EventsPostMutation,
  useReadEventV1EventsEventIdGetQuery,
  useUpdateEventV1EventsEventIdPutMutation,
  useDeleteEventV1EventsEventIdDeleteMutation,
} = injectedRtkApi;
