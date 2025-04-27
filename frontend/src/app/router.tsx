import { createBrowserRouter } from 'react-router';
import { CalendarPage } from '@pages/CalendarPage';
import { EventsFeedPage } from '@pages/EventsFeedPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <CalendarPage />,
  },
  {
    path: '/feed',
    element: <EventsFeedPage />,
  },
]);
