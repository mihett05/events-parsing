import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { CalendarEvent, mapEventToCalendarEvent } from '@entities/Event';
import { createEntityAdapter } from '@reduxjs/toolkit';
import { api } from '@shared/api/api';

export const eventsAdapter = createEntityAdapter<CalendarEvent>();

type FilterState = {
  start: Date | null;
  end: Date | null;
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
  error: string | null;
  page: number;
  pageSize: number;
  selectedDate: Date;
  filters: FilterState;
  filterVariants: FilterVariants;
}

const initialState: EventsState = {
  events: eventsAdapter.getInitialState(),
  page: 0,
  pageSize: 20,
  isLoading: false,
  error: null,
  selectedDate: new Date(),
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

const eventsSlice = createSlice({
  name: 'events',
  initialState,
  reducers: {
    upsertEvents: (state, action: PayloadAction<CalendarEvent[]>) => {
      eventsAdapter.upsertMany(state.events, action.payload);
    },
    incrementPage: (state) => {
      if (state.isLoading) return;
      state.page++;
    },
    setSelectedDate: (state, action: PayloadAction<Date>) => {
      state.selectedDate = action.payload;
    },
    setFilters: (state, filter: PayloadAction<FilterState>) => {
      state.filters = filter.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(
        api.endpoints.readAllEventsV1EventsFeedGet.matchFulfilled,
        (state, { payload }) => {
          state.isLoading = false;
          eventsAdapter.upsertMany(state.events, payload.map(mapEventToCalendarEvent));
          updateFilterVariants(state);
        },
      )
      .addMatcher(api.endpoints.readAllEventsV1EventsFeedGet.matchPending, (state) => {
        state.isLoading = true;
      })
      .addMatcher(api.endpoints.readAllEventsV1EventsFeedGet.matchRejected, (state, { error }) => {
        state.isLoading = false;
        state.error = error.message ?? null;
      })
      .addMatcher(api.endpoints.readAllEventsV1EventsCalendarGet.matchPending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addMatcher(
        api.endpoints.readAllEventsV1EventsCalendarGet.matchFulfilled,
        (state, { payload }) => {
          state.isLoading = false;
          eventsAdapter.setAll(state.events, payload.map(mapEventToCalendarEvent));
          updateFilterVariants(state);
        },
      )
      .addMatcher(
        api.endpoints.readAllEventsV1EventsCalendarGet.matchRejected,
        (state, { error }) => {
          state.isLoading = false;
          state.error = error.message ?? 'Ошибка загрузки календаря';
        },
      );
  },
});

const updateFilterVariants = (state: EventsState) => {
  const events = eventsAdapter.getSelectors().selectAll(state.events);
  const formats = new Set();
  const types = new Set();

  events.forEach((event) => {
    formats.add(event.format);
    types.add(event.type);
  });

  state.filterVariants = {
    formats: Array.from(formats.values()) as string[],
    types: Array.from(types.values()) as string[],
  };
};

export const { upsertEvents, incrementPage, setSelectedDate } = eventsSlice.actions;
export default eventsSlice.reducer;
