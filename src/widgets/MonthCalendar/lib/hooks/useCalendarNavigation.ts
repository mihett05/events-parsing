import { useState, useCallback } from 'react';
import { addMonths, subMonths } from 'date-fns';

interface UseCalendarNavigationProps {
  initialDate?: Date;
}

export const useCalendarNavigation = ({ initialDate = new Date() }: UseCalendarNavigationProps) => {
  const [currentDate, setCurrentDate] = useState<Date>(initialDate);

  const handlePrevMonth = useCallback(() => {
    setCurrentDate((prev) => subMonths(prev, 1));
  }, []);

  const handleNextMonth = useCallback(() => {
    setCurrentDate((prev) => addMonths(prev, 1));
  }, []);

  const handleToday = useCallback(() => {
    setCurrentDate(new Date());
  }, []);

  return {
    currentDate,
    handlePrevMonth,
    handleNextMonth,
    handleToday,
  };
};
