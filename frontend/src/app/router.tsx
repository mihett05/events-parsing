import { createBrowserRouter } from 'react-router';
import { CalendarPage } from '@pages/CalendarPage';
import { EventsFeedPage } from '@pages/EventsFeedPage';
import { AppPaths } from '@/shared/routes';

export const router = createBrowserRouter([
  {
    path: AppPaths.calendar(),
    element: <CalendarPage />,
  },
  {
    path: AppPaths.eventsFeed(),
    element: <EventsFeedPage />,
  },
]);
