import { CalendarEvent, mapEventToCalendarEvent } from '@/entities/Event';
import { api } from '@/shared/api/api';
import { createEntityAdapter, createSlice, PayloadAction } from '@reduxjs/toolkit';

export const calendarEventsAdapter = createEntityAdapter<CalendarEvent>();

interface CalendarEventsState {
  events: ReturnType<typeof calendarEventsAdapter.getInitialState>;
  isLoading: boolean;
  error: string | null;
  selectedDate: string; // ISO string
}

const initialDate = new Date();
initialDate.setUTCHours(0, 0, 0, 0);

const initialState: CalendarEventsState = {
  events: calendarEventsAdapter.getInitialState(),
  selectedDate: initialDate.toISOString(),
  isLoading: false,
  error: null,
};

const calendarEventsSlice = createSlice({
  name: 'calendarEvents',
  initialState,
  reducers: {
    setSelectedDate: (state, action: PayloadAction<string>) => {
      state.selectedDate = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(api.endpoints.readAllEventsV1EventsCalendarGet.matchPending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addMatcher(
        api.endpoints.readAllEventsV1EventsCalendarGet.matchFulfilled,
        (state, { payload }) => {
          state.isLoading = false;
          calendarEventsAdapter.setAll(state.events, payload.map(mapEventToCalendarEvent));
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

export const { setSelectedDate } = calendarEventsSlice.actions;
export default calendarEventsSlice.reducer;