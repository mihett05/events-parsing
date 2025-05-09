import { useSelector, useDispatch } from 'react-redux';
import { useReadAllEventsV1EventsCalendarGetQuery } from '@/shared/api/api';
import {
  selectSelectedDate,
  selectCalendarView,
  setSelectedDate as setSelectedDateAction,
  CalendarView,
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
      const monthStart = startOfMonth(date);
      start = subMonths(monthStart, 1);
      const monthEnd = endOfMonth(date);
      end = addMonths(monthEnd, 1);
      end = endOfDay(end);
      break;
  }

  return {
    startDate: formatDateFns(start, 'yyyy-MM-dd'),
    endDate: formatDateFns(end, 'yyyy-MM-dd'),
  };
};

export const useCalendarViewData = () => {
  const dispatch = useDispatch();
  const selectedDateString = useSelector(selectSelectedDate);
  const calendarView = useSelector(selectCalendarView);

  const currentDate = new Date(selectedDateString);

  const dateRange = getCalendarDateRange(currentDate, calendarView);

  const apiStartDate = dateRange?.startDate
    ? formatDateFns(dateRange.startDate, 'yyyy-MM-dd')
    : undefined;
  const apiEndDate = dateRange?.endDate
    ? formatDateFns(dateRange.endDate, 'yyyy-MM-dd')
    : undefined;

  const { isLoading, error, refetch } = useReadAllEventsV1EventsCalendarGetQuery(
    {
      startDate: apiStartDate,
      endDate: apiEndDate,
    },
    {
      skip: !apiStartDate || !apiEndDate || !isValid(currentDate),
    },
  );

  const handlePrev = () => {
    if (!isValid(currentDate)) return;
    let newDate;
    if (calendarView === 'year') newDate = subYears(currentDate, 1);
    else if (calendarView === 'month') newDate = subMonths(currentDate, 1);
    else newDate = subDays(currentDate, 1);
    dispatch(setSelectedDateAction(newDate.toISOString()));
  };

  const handleNext = () => {
    if (!isValid(currentDate)) return;
    let newDate;
    if (calendarView === 'year') newDate = addYears(currentDate, 1);
    else if (calendarView === 'month') newDate = addMonths(currentDate, 1);
    else newDate = addDays(currentDate, 1);
    dispatch(setSelectedDateAction(newDate.toISOString()));
  };

  const handleToday = () => {
    dispatch(setSelectedDateAction(new Date().toISOString()));
  };

  const parsedError = error
    ? (error as any)?.data?.detail?.[0]?.msg ||
      (error as any)?.data?.message ||
      (error as any)?.status ||
      'Произошла ошибка загрузки'
    : null;

  return {
    currentDate: isValid(currentDate) ? currentDate : new Date(),
    isLoading,
    error: parsedError,
    calendarView,
    handlePrev,
    handleNext,
    handleToday,
    refetchCalendarEvents: refetch,
  };
};
