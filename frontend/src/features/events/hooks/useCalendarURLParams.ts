import { useParams, useSearchParams } from 'react-router';
import { useMemo } from 'react';
import { CalendarView, FilterState, selectFilterVariants } from '@/features/events/slice';
import { parseISO, isValid as isValidDate } from 'date-fns';
import { useAppSelector } from '@/shared/store/hooks';
import { EventFormatEnum, EventTypeEnum } from '@/shared/api/api';

export const useCalendarUrlParams = (): {
  currentCalendarView: CalendarView;
  currentDate: Date;
  activeFilters: FilterState;
  isInitialRedirectNeeded: boolean;
} => {
  const params = useParams<{ calendarView?: string; date?: string }>();
  const [searchParams] = useSearchParams();
  const filterVariants = useAppSelector(selectFilterVariants);

  const currentCalendarView = useMemo((): CalendarView => {
    const view = params.calendarView;
    if (view && (view === 'day' || view === 'month' || view === 'year')) {
      return view as CalendarView;
    }
    return 'month';
  }, [params.calendarView]);

  const currentDate = useMemo(() => {
    const dateStr = params.date;
    if (dateStr) {
      const parsed = parseISO(dateStr);
      if (isValidDate(parsed)) {
        return parsed;
      }
    }
    return new Date();
  }, [params.date]);

  const activeFilters = useMemo((): FilterState => {
    const type = searchParams.get('type') as EventTypeEnum | null;
    const format = searchParams.get('format') as EventFormatEnum | null;
    const organizationName = searchParams.get('organization');

    let organizationId: number | null = null;
    if (organizationName && filterVariants.organizations.length > 0) {
      const foundOrg = filterVariants.organizations.find((org) => org.title === organizationName);
      organizationId = foundOrg ? foundOrg.id : null;
    }

    return {
      type: type || null,
      format: format || null,
      organizationId,
    };
  }, [searchParams, filterVariants.organizations]);

  const isInitialRedirectNeeded = !params.calendarView || !params.date;

  return { currentCalendarView, currentDate, activeFilters, isInitialRedirectNeeded };
};
