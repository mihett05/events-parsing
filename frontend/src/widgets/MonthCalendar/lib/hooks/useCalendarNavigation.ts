import { useState, useCallback, useEffect } from 'react';
import { addMonths, subMonths, isValid, isEqual } from 'date-fns';

interface UseCalendarNavigationProps {
  selectedDate?: Date;
  onMonthChange?: (newDate: Date) => void;
}

export const useCalendarNavigation = ({
  selectedDate = new Date(),
  onMonthChange,
}: UseCalendarNavigationProps) => {
  const normalizeDate = useCallback((date: Date | undefined): Date => {
    const validDate = date && isValid(date) ? date : new Date();
    const utcDate = new Date(Date.UTC(validDate.getFullYear(), validDate.getMonth(), 1));
    return utcDate;
  }, []);

  const [currentDate, setCurrentDate] = useState<Date>(() => normalizeDate(selectedDate));

  useEffect(() => {
    const normalizedPropDate = normalizeDate(selectedDate);
    if (!isEqual(normalizedPropDate, currentDate)) {
      setCurrentDate(normalizedPropDate);
    }
  }, [selectedDate, normalizeDate, currentDate]);

  const handlePrevMonth = useCallback(() => {
    const newDate = subMonths(currentDate, 1);
    onMonthChange?.(newDate);
  }, [currentDate, onMonthChange]);

  const handleNextMonth = useCallback(() => {
    const newDate = addMonths(currentDate, 1);
    onMonthChange?.(newDate);
  }, [currentDate, onMonthChange]);

  const handleToday = useCallback(() => {
    const newDate = new Date();
    const normalizedToday = normalizeDate(newDate);
    onMonthChange?.(normalizedToday);
  }, [onMonthChange, normalizeDate]);

  return {
    currentDate: isValid(currentDate) ? currentDate : new Date(),
    handlePrevMonth,
    handleNextMonth,
    handleToday,
  };
};
