import { createSlice, PayloadAction, createEntityAdapter } from '@reduxjs/toolkit';
import { CalendarEvent } from '@entities/Event';
import { api } from '@shared/api/api';
import { mapEventToCalendarEvent } from '@entities/Event/model/mappers';
import { RootState } from '@/shared/store/store';

export const eventsAdapter = createEntityAdapter<CalendarEvent>();

export type CalendarView = 'day' | 'month' | 'year';

type FilterState = {
  start: string | null;
  end: string | null;
  type: string | null;
  format: string | null;
};
type FilterVariants = {
  types: string[];
  formats: string[];
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
    start: null,
    end: null,
    type: null,
    format: null,
  },
  filterVariants: {
    formats: [],
    types: [],
  },
};

const updateFilterVariants = (state: EventsState) => {
  const events = eventsAdapter.getSelectors().selectAll(state.events);
  const formats = new Set<string>();
  const types = new Set<string>();

  events.forEach((event) => {
    if (event.format) formats.add(event.format);
    if (event.type) types.add(event.type);
  });

  const newFormats = Array.from(formats);
  const newTypes = Array.from(types);

  if (
    JSON.stringify(state.filterVariants.formats) !== JSON.stringify(newFormats) ||
    JSON.stringify(state.filterVariants.types) !== JSON.stringify(newTypes)
  ) {
    state.filterVariants = { formats: newFormats, types: newTypes };
  }
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
        // eventsAdapter.removeAll(state.events);
      }
    },
    setFilters: (state, action: PayloadAction<Partial<FilterState>>) => {
      const newFilters = { ...state.filters, ...action.payload };
      if (JSON.stringify(state.filters) !== JSON.stringify(newFilters)) {
        state.filters = newFilters;
        state.page = 0;
        state.events = eventsAdapter.getInitialState();
        state.error = null;
      }
    },
    resetFilters: (state) => {
      if (JSON.stringify(state.filters) !== JSON.stringify(initialState.filters)) {
        state.filters = initialState.filters;
        state.page = 0;
        state.events = eventsAdapter.getInitialState();
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
          updateFilterVariants(state);
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
          updateFilterVariants(state);
        },
      )
      .addMatcher(
        api.endpoints.readAllEventsV1EventsCalendarGet.matchRejected,
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
export const selectCalendarView = (state: RootState) => state.events.calendarView;
