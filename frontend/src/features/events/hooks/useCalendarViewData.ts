import { useReadAllEventsV1EventsGetQuery } from '@/shared/api/api';
import {
  CalendarView,
  FilterState,
  selectEventsLoading,
  selectEventsError,
  selectFilteredEvents,
} from '@/features/events/slice';
import {
  startOfYear,
  endOfYear,
  addYears,
  subYears,
  startOfMonth,
  endOfMonth,
  addMonths,
  subMonths,
  startOfDay,
  endOfDay,
  addDays,
  subDays,
  isValid,
  format as formatDateFns,
} from 'date-fns';
import { useAppSelector } from '@/shared/store/hooks';
import { CalendarNavOptions } from '@/widgets/CalendarCommon/types';

const getCalendarDateRange = (
  date: Date,
  view: CalendarView,
): { startDate: string; endDate: string } => {
  let start: Date;
  let end: Date;

  switch (view) {
    case 'day':
      start = startOfDay(date);
      end = endOfDay(date);
      break;
    case 'year':
      start = startOfYear(date);
      end = endOfYear(date);
      break;
    case 'month':
    default:
      const monthStartAnchor = startOfMonth(date);
      start = subMonths(monthStartAnchor, 1);
      const monthEndAnchor = endOfMonth(date);
      end = addMonths(monthEndAnchor, 1);
      end = endOfDay(end);
      break;
  }
  return {
    startDate: formatDateFns(start, 'yyyy-MM-dd'),
    endDate: formatDateFns(end, 'yyyy-MM-dd'),
  };
};

export const useCalendarViewData = (
  currentView: CalendarView,
  currentDate: Date,
  activeFiltersForClientSide: FilterState,
  onNavigate: (options: CalendarNavOptions) => void,
) => {
  const dateRange = getCalendarDateRange(currentDate, currentView);
  const apiStartDate = dateRange.startDate;
  const apiEndDate = dateRange.endDate;

  const { refetch } = useReadAllEventsV1EventsGetQuery(
    {
      startDate: apiStartDate,
      endDate: apiEndDate,
    },
    {
      skip: !apiStartDate || !apiEndDate || !isValid(currentDate),
    },
  );

  const reduxIsLoading = useAppSelector(selectEventsLoading);
  const reduxError = useAppSelector(selectEventsError);
  const filteredEvents = useAppSelector((state) =>
    selectFilteredEvents(state, activeFiltersForClientSide),
  );

  const handlePrev = () => {
    if (!isValid(currentDate)) return;
    let newDate;
    if (currentView === 'year') newDate = subYears(currentDate, 1);
    else if (currentView === 'month') newDate = subMonths(currentDate, 1);
    else newDate = subDays(currentDate, 1);
    onNavigate({ date: newDate });
  };

  const handleNext = () => {
    if (!isValid(currentDate)) return;
    let newDate;
    if (currentView === 'year') newDate = addYears(currentDate, 1);
    else if (currentView === 'month') newDate = addMonths(currentDate, 1);
    else newDate = addDays(currentDate, 1);
    onNavigate({ date: newDate });
  };

  const handleToday = () => {
    onNavigate({ date: new Date() });
  };

  const handleViewChange = (newView: CalendarView) => {
    onNavigate({ view: newView });
  };

  return {
    events: filteredEvents,
    isLoading: reduxIsLoading,
    error: reduxError,
    handlePrev,
    handleNext,
    handleToday,
    handleViewChange,
    refetchCalendarEvents: refetch,
  };
};
