import { createBrowserRouter } from 'react-router';
import { CalendarPage } from '@pages/CalendarPage/CalendarPage';
import { EventsFeedPage } from '@/pages/EventsFeedPage/EventsFeedPage';
import { AppPaths } from '@/shared/routes';
import { RegisterPage } from '@/pages/RegisterPage';
import { LoginPage } from '@/pages/LoginPage';
import { ProfilePage } from '@/pages/ProfilePage';
import { OrganizationsPage } from '@/pages/OrganizationsPage';
import { OrganizationPage } from '@/pages/OrganizationPage';
import { EventEditPage } from '@/pages/EventEditPage';
import { EventCreatePage } from '@/pages/EventCreatePage';

export const router = createBrowserRouter([
  {
    path: AppPaths.eventsFeed(),
    element: <EventsFeedPage />,
  },
  {
    path: '/:calendarView/:date',
    element: <CalendarPage />,
  },
  {
    path: '/:calendarView',
    element: <CalendarPage />,
  },
  {
    path: AppPaths.calendarBase(),
    element: <CalendarPage />,
  },
  {
    path: AppPaths.register(),
    element: <RegisterPage />,
  },
  {
    path: AppPaths.login(),
    element: <LoginPage />,
  },
  {
    path: AppPaths.profile(),
    element: <ProfilePage />,
  },
  {
    path: AppPaths.organizations(),
    element: <OrganizationsPage />,
  },
  {
    path: '/organizations/:organizationId',
    element: <OrganizationPage />,
  },
  {
    path: '/organizations/:organizationId/events',
    element: <OrganizationPage />,
  },
  {
    path: '/events/:eventId',
    element: <EventEditPage />,
  },
  {
    path: '/events',
    element: <EventCreatePage />,
  },
]);
