import { format as formatDateFns, parseISO, isValid as isValidDate } from 'date-fns';
import type { CalendarView as AppCalendarView } from '@/features/events/slice';

interface FilterUrlParams {
  type?: string | null;
  format?: string | null;
  organization?: string | null;
  [key: string]: string | number | null | undefined;
}

const getCalendarPath = (
  calendarView?: AppCalendarView | string,
  date?: string | Date,
  filters?: FilterUrlParams,
): string => {
  const actualView = calendarView || 'month';
  const dateObj = date instanceof Date ? date : date ? parseISO(date) : new Date();
  const actualDateStr = isValidDate(dateObj)
    ? formatDateFns(dateObj, 'yyyy-MM-dd')
    : formatDateFns(new Date(), 'yyyy-MM-dd');

  let path = `/${actualView}/${actualDateStr}`;

  if (filters) {
    const queryParams = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && String(value).trim() !== '') {
        queryParams.set(key, String(value));
      }
    });
    const qs = queryParams.toString();
    if (qs) {
      path += `?${qs}`;
    }
  }
  return path;
};

const getOrganizationsPath = () => '/organizations';
const getOrganizationPath = (organizationId: number) =>
  `${getOrganizationsPath()}/${organizationId}`;
const getEventsPath = (organizationId: number) => `${getOrganizationPath(organizationId)}/events`;
const getEventPath = (eventId: number) => `/events/${eventId}`;
const getUsersPath = (organizationId: number) => `${getOrganizationPath(organizationId)}/users`;
const getUserPath = (organizationId: number, userId: number) =>
  `${getUsersPath(organizationId)}/${userId}`;

export const AppPaths = {
  calendarBase: () => '/',
  calendar: getCalendarPath,
  eventsFeed: () => '/feed',
  profile: () => '/profile',
  login: () => '/auth/login',
  register: () => '/auth/register',
  organizations: getOrganizationsPath,
  organization: getOrganizationPath,
  events: getEventsPath,
  event: getEventPath,
  users: getUsersPath,
  user: getUserPath,
};
