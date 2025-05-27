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

export const AppPaths = {
  calendarBase: () => '/',
  calendar: getCalendarPath,
  eventsFeed: () => '/feed',
  profile: () => '/profile',
  login: () => '/auth/login',
  register: () => '/auth/register',
};
