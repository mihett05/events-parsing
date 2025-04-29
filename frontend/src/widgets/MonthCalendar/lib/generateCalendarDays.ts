import {
  startOfMonth,
  startOfWeek,
  eachDayOfInterval,
  isSameMonth,
  isToday as isTodayDateFns,
  isSunday,
  isSaturday,
  addDays,
} from 'date-fns';
import { CalendarDayData } from '@shared/lib/types';

const WEEKS_TO_DISPLAY = 6;

export const generateCalendarDays = (currentMonthDate: Date): CalendarDayData[] => {
  const monthStart = startOfMonth(currentMonthDate);
  const gridStartDate = startOfWeek(monthStart, { weekStartsOn: 0 });
  const gridEndDate = addDays(gridStartDate, WEEKS_TO_DISPLAY * 7 - 1);

  const days = eachDayOfInterval({
    start: gridStartDate,
    end: gridEndDate,
  });

  return days.map((day): CalendarDayData => {
    const isWeekend = isSunday(day) || isSaturday(day);
    return {
      date: day,
      isCurrentMonth: isSameMonth(day, currentMonthDate),
      isToday: isTodayDateFns(day),
      isWeekend: isWeekend,
    };
  });
};

export const getDayNames = (weekStartsOn: 0 | 1 = 0): string[] => {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  if (weekStartsOn === 1) {
    return [...days.slice(1), days[0]];
  }
  return days;
};
