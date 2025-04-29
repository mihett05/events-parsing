import { configureStore } from '@reduxjs/toolkit';
import { api } from '../api/api';
import eventsReducer from '@features/events/slice';
import calendarEventsReducer from '@features/events/calendarSlice';
export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    events: eventsReducer,
    calendarEvents: calendarEventsReducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(api.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;