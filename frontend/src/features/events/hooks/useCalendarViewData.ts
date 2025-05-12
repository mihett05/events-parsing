import { useMemo, useCallback } from 'react';
import { useAppDispatch, useAppSelector } from '@/shared/store/hooks';
import {
  setSelectedDate,
  eventsSelectors,
  selectSelectedDate,
  selectEventsLoading,
  selectEventsError,
  selectCalendarView,
  CalendarView,
} from '@features/events/slice';
import { useReadAllEventsV1EventsCalendarGetQuery } from '@/shared/api/api';
import {
  addMonths,
  subMonths,
  addDays,
  subDays,
  addYears,
  subYears,
  isValid,
  startOfMonth,
  endOfMonth,
  parseISO,
  startOfDay,
  endOfDay,
  startOfYear,
  endOfYear,
  isEqual,
  format,
} from 'date-fns';

const getApiDateRange = (
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
    startDate: format(start, 'yyyy-MM-dd'),
    endDate: format(end, 'yyyy-MM-dd'),
  };
};

export const useCalendarViewData = () => {
  const dispatch = useAppDispatch();

  const selectedDateISO = useAppSelector(selectSelectedDate);
  const calendarView = useAppSelector(selectCalendarView);
  const events = useAppSelector(eventsSelectors.selectAll);
  const isSliceLoading = useAppSelector(selectEventsLoading);
  const sliceErrorKey = useAppSelector(selectEventsError);

  const currentDate = useMemo(() => {
    try {
      const parsed = parseISO(selectedDateISO);
      return isValid(parsed) ? parsed : new Date();
    } catch {
      console.error('Failed to parse selectedDateISO:', selectedDateISO);
      return new Date();
    }
  }, [selectedDateISO]);

  const { startDate: apiQueryStartDate, endDate: apiQueryEndDate } = useMemo(() => {
    return getApiDateRange(currentDate, calendarView);
  }, [currentDate, calendarView]);

  const {
    isFetching,
    error: queryError,
    isLoading: isQueryLoading,
  } = useReadAllEventsV1EventsCalendarGetQuery(
    {
      startDate: apiQueryStartDate,
      endDate: apiQueryEndDate,
    },
    {
      skip: !apiQueryStartDate || !apiQueryEndDate,
    },
  );

  const handleDateChange = useCallback(
    (newDate: Date) => {
      if (isValid(newDate)) {
        if (!isEqual(startOfDay(newDate), startOfDay(currentDate))) {
          dispatch(setSelectedDate(newDate.toISOString()));
        }
      } else {
        console.warn('Attempted to set invalid date:', newDate);
      }
    },
    [dispatch, currentDate],
  );

  const handlePrev = useCallback(() => {
    let newDate: Date;
    switch (calendarView) {
      case 'day':
        newDate = subDays(currentDate, 1);
        break;
      case 'year':
        newDate = subYears(currentDate, 1);
        break;
      case 'month':
      default:
        newDate = subMonths(currentDate, 1);
        break;
    }
    handleDateChange(newDate);
  }, [calendarView, currentDate, handleDateChange]);

  const handleNext = useCallback(() => {
    let newDate: Date;
    switch (calendarView) {
      case 'day':
        newDate = addDays(currentDate, 1);
        break;
      case 'year':
        newDate = addYears(currentDate, 1);
        break;
      case 'month':
      default:
        newDate = addMonths(currentDate, 1);
        break;
    }
    handleDateChange(newDate);
  }, [calendarView, currentDate, handleDateChange]);

  const handleToday = useCallback(() => {
    handleDateChange(new Date());
  }, [handleDateChange]);

  const isLoading = isSliceLoading || (isQueryLoading && events.length === 0);
  const isBackgroundFetching = isFetching && !isLoading;

  const error = sliceErrorKey
    ? { messageKey: sliceErrorKey, messageOptions: { message: String(queryError) || '' } }
    : null;

  return {
    currentDate: isValid(currentDate) ? currentDate : new Date(),
    events,
    isLoading,
    isBackgroundFetching,
    error,
    calendarView,
    handlePrev,
    handleNext,
    handleToday,
  };
};
