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
  selectedDate: string;
  calendarView: CalendarView;
  filters: FilterState;
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
  selectedDate: new Date().toISOString(),
  calendarView: 'month',
  filters: {
    format: null,
    type: null,
    organizationId: null,
  },
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
    incrementPage: (state) => {
      if (!state.isLoading && !state.isFetchingMore) {
        state.page++;
      }
    },
    setSelectedDate: (state, action: PayloadAction<string>) => {
      if (state.selectedDate !== action.payload) {
        state.selectedDate = action.payload;
        state.error = null;
      }
    },
    setCalendarView: (state, action: PayloadAction<CalendarView>) => {
      if (state.calendarView !== action.payload) {
        state.calendarView = action.payload;
        state.error = null;
        state.page = 0;
      }
    },
    setFilters: (state, action: PayloadAction<Partial<FilterState>>) => {
      const currentFilters = state.filters;
      const newPartialFilters = action.payload;
      let filtersChanged = false;
      if (
        newPartialFilters.hasOwnProperty('type') &&
        currentFilters.type !== newPartialFilters.type
      ) {
        currentFilters.type = newPartialFilters.type!;
        filtersChanged = true;
      }
      if (
        newPartialFilters.hasOwnProperty('format') &&
        currentFilters.format !== newPartialFilters.format
      ) {
        currentFilters.format = newPartialFilters.format!;
        filtersChanged = true;
      }
      if (
        newPartialFilters.hasOwnProperty('organizationId') &&
        currentFilters.organizationId !== newPartialFilters.organizationId
      ) {
        currentFilters.organizationId = newPartialFilters.organizationId as number | null;
        filtersChanged = true;
      }
      if (filtersChanged) {
        state.error = null;
      }
    },
    resetFilters: (state) => {
      let filtersChanged = false;
      if (state.filters.type !== initialState.filters.type) {
        state.filters.type = initialState.filters.type;
        filtersChanged = true;
      }
      if (state.filters.format !== initialState.filters.format) {
        state.filters.format = initialState.filters.format;
        filtersChanged = true;
      }
      if (state.filters.organizationId !== initialState.filters.organizationId) {
        state.filters.organizationId = initialState.filters.organizationId;
        filtersChanged = true;
      }
      if (filtersChanged) {
        state.error = null;
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

export const {
  incrementPage,
  setSelectedDate,
  setCalendarView,
  setFilters,
  resetFilters,
  clearError,
} = eventsSlice.actions;
export default eventsSlice.reducer;

export const getEventsState = (state: RootState) => state.events;

export const eventsSelectors = eventsAdapter.getSelectors<RootState>(
  (state) => state.events.events,
);

export const selectEventsLoading = (state: RootState) => state.events.isLoading;
export const selectEventsFetchingMore = (state: RootState) => state.events.isFetchingMore;
export const selectEventsError = (state: RootState) => state.events.error;
export const selectEventsCurrentPage = (state: RootState) => state.events.page;
export const selectSelectedDate = (state: RootState) => state.events.selectedDate;
export const selectFilterVariants = (state: RootState) => state.events.filterVariants;
export const selectActiveFilters = (state: RootState) => state.events.filters;
export const selectAreFilterVariantsLoaded = (state: RootState) =>
  state.events.areFilterVariantsLoaded;
export const selectCalendarView = (state: RootState) => state.events.calendarView;

export const selectFilteredCalendarEvents = createSelector(
  [eventsSelectors.selectAll, selectActiveFilters],
  (allEvents, filters) => {
    if (filters.type === null && filters.format === null && filters.organizationId === null) {
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
