import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { CalendarEvent, mapEventToCalendarEvent } from '@entities/Event';
import { createEntityAdapter } from '@reduxjs/toolkit';
import { api } from '@shared/api/api';

export const eventsAdapter = createEntityAdapter<CalendarEvent>();

interface EventsState {
  events: ReturnType<typeof eventsAdapter.getInitialState>;
  isLoading: boolean;
  error: string | null;
  page: number;
  pageSize: number;
}

const initialState: EventsState = {
  events: eventsAdapter.getInitialState(),
  page: 0,
  pageSize: 20,
  isLoading: false,
  error: null,
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
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(api.endpoints.readAllEventsV1EventsGet.matchFulfilled, (state, { payload }) => {
        state.isLoading = false;
        eventsAdapter.upsertMany(state.events, payload.map(mapEventToCalendarEvent));
      })
      .addMatcher(api.endpoints.readAllEventsV1EventsGet.matchPending, (state) => {
        state.isLoading = true;
      })
      .addMatcher(api.endpoints.readAllEventsV1EventsGet.matchRejected, (state, { error }) => {
        state.isLoading = false;
        state.error = error.message ?? null;
      });
  },
});

export const { upsertEvents, incrementPage } = eventsSlice.actions;
export default eventsSlice.reducer;
