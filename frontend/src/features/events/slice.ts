import { createSlice, PayloadAction, createEntityAdapter, createSelector } from '@reduxjs/toolkit';
import { CalendarEvent } from '@entities/Event';
import { api, EventFormatEnum, EventTypeEnum, FilterModel } from '@shared/api/api';
import { mapEventToCalendarEvent } from '@entities/Event/model/mappers';
import { RootState } from '@/shared/store/store';

export const eventsAdapter = createEntityAdapter<CalendarEvent>();

export type CalendarView = 'day' | 'month' | 'year';

export type FilterState = {
  type: EventTypeEnum | null;
  format: EventFormatEnum | null;
  organizationId: number | null;
};

export interface OrganizationFilterOption {
  id: number;
  title: string;
}

export type FilterVariants = {
  types: EventTypeEnum[];
  formats: EventFormatEnum[];
  organizations: OrganizationFilterOption[];
};

interface EventsState {
  events: ReturnType<typeof eventsAdapter.getInitialState>;
  isLoading: boolean;
  isFetchingMore: boolean;
  error: string | null;
  page: number;
  pageSize: number;
  filterVariants: FilterVariants;
  areFilterVariantsLoaded: boolean;
}

const initialState: EventsState = {
  events: eventsAdapter.getInitialState(),
  page: 0,
  pageSize: 20,
  isLoading: false,
  isFetchingMore: false,
  error: null,
  filterVariants: {
    formats: [],
    types: [],
    organizations: [],
  },
  areFilterVariantsLoaded: false,
};

const eventsSlice = createSlice({
  name: 'events',
  initialState,
  reducers: {
    setPage: (state, action: PayloadAction<number>) => {
      state.page = action.payload;
    },
    incrementPage: (state) => {
      if (!state.isLoading && !state.isFetchingMore) {
        state.page++;
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(api.endpoints.readAllEventsV1EventsFeedGet.matchPending, (state, { meta }) => {
        if (meta.arg.originalArgs?.page === 0) {
          state.isLoading = true;
        } else {
          state.isFetchingMore = true;
        }
        state.error = null;
      })
      .addMatcher(
        api.endpoints.readAllEventsV1EventsFeedGet.matchFulfilled,
        (state, { payload, meta }) => {
          state.isLoading = false;
          state.isFetchingMore = false;
          const newEvents = payload.map(mapEventToCalendarEvent).filter(Boolean) as CalendarEvent[];
          if (meta.arg.originalArgs?.page === 0) {
            eventsAdapter.setAll(state.events, newEvents);
          } else {
            eventsAdapter.addMany(state.events, newEvents);
          }
        },
      )
      .addMatcher(api.endpoints.readAllEventsV1EventsFeedGet.matchRejected, (state) => {
        state.isLoading = false;
        state.isFetchingMore = false;
        state.error = 'feed.errorLoading';
      })
      .addMatcher(api.endpoints.readAllEventsV1EventsCalendarGet.matchPending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addMatcher(
        api.endpoints.readAllEventsV1EventsCalendarGet.matchFulfilled,
        (state, { payload }) => {
          state.isLoading = false;
          const mappedEvents = payload
            .map(mapEventToCalendarEvent)
            .filter(Boolean) as CalendarEvent[];
          eventsAdapter.upsertMany(state.events, mappedEvents);
        },
      )
      .addMatcher(
        api.endpoints.readAllEventsV1EventsCalendarGet.matchRejected,
        (state, { error }) => {
          state.isLoading = false;
          state.error = error.message ?? 'calendar.errorLoading';
        },
      )
      .addMatcher(api.endpoints.getTypesAndFormatsV1EventsFeedFiltersGet.matchPending, (state) => {
        state.isLoading = true;
      })
      .addMatcher(
        api.endpoints.getTypesAndFormatsV1EventsFeedFiltersGet.matchFulfilled,
        (state, action: PayloadAction<FilterModel>) => {
          state.filterVariants.types = action.payload.type ? [...action.payload.type] : [];
          state.filterVariants.formats = action.payload.format ? [...action.payload.format] : [];
          state.filterVariants.organizations = action.payload.organization
            ? action.payload.organization.map((org) => ({ id: org.id, title: org.title }))
            : [];
          state.areFilterVariantsLoaded = true;
          state.error = null;
        },
      )
      .addMatcher(
        api.endpoints.getTypesAndFormatsV1EventsFeedFiltersGet.matchRejected,
        (state, { error }) => {
          state.isLoading = false;
          state.error = error.message ?? 'calendar.errorLoading';
        },
      );
  },
});

export const { setPage, incrementPage, clearError } = eventsSlice.actions;
export default eventsSlice.reducer;

export const getEventsState = (state: RootState) => state.events;

export const eventsSelectors = eventsAdapter.getSelectors<RootState>(
  (state) => state.events.events,
);

export const selectAllEvents = eventsSelectors.selectAll;

export const selectEventsLoading = (state: RootState) => state.events.isLoading;
export const selectEventsFetchingMore = (state: RootState) => state.events.isFetchingMore;
export const selectEventsError = (state: RootState) => state.events.error;
export const selectEventsCurrentPage = (state: RootState) => state.events.page;
export const selectFilterVariants = (state: RootState) => state.events.filterVariants;
export const selectAreFilterVariantsLoaded = (state: RootState) =>
  state.events.areFilterVariantsLoaded;

export const selectFilteredEvents = createSelector(
  [selectAllEvents, (_state: RootState, filters: FilterState | null | undefined) => filters],
  (allEvents, filters) => {
    if (
      !filters ||
      (filters.type === null && filters.format === null && filters.organizationId === null)
    ) {
      return allEvents;
    }
    return allEvents.filter((event) => {
      const typeMatch = filters.type === null || event.type === filters.type;
      const formatMatch = filters.format === null || event.format === filters.format;
      const organizationMatch =
        filters.organizationId === null || event.organizationId === filters.organizationId;
      return typeMatch && formatMatch && organizationMatch;
    });
  },
);
