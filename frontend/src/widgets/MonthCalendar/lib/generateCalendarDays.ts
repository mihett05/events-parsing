import {
  startOfMonth,
  startOfWeek,
  eachDayOfInterval,
  isSameMonth,
  isToday as isTodayDateFns,
  isSunday,
  isSaturday,
  addDays,
  format,
} from 'date-fns';
import { ru } from 'date-fns/locale';
import { CalendarDayData } from '@shared/lib/types';
import { useTranslation } from 'react-i18next';

const WEEKS_TO_DISPLAY = 6;

export const generateCalendarDays = (
  currentMonthDate: Date,
  weekStartsOn: 0 | 1 = 1,
): CalendarDayData[] => {
  const monthStart = startOfMonth(currentMonthDate);
  const gridStartDate = startOfWeek(monthStart, { weekStartsOn });
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

export const useLocalizedDayNames = (weekStartsOn: 0 | 1 = 1): string[] => {
  const { t, i18n } = useTranslation();
  const localizedDayNames = t('calendar.dayNames', { returnObjects: true }) as string[];

  if (!Array.isArray(localizedDayNames) || localizedDayNames.length !== 7) {
    console.warn('Translation for calendar.dayNames is not an array of 7 strings. Using fallback.');
    const locale = i18n.language.startsWith('ru') ? ru : undefined;
    const fallbackNames: string[] = [];
    const baseDate = startOfWeek(new Date(2023, 0, 1), { weekStartsOn });
    for (let i = 0; i < 7; i++) {
      fallbackNames.push(format(addDays(baseDate, i), 'EEEEEE', { locale }));
    }
    return fallbackNames;
  }

  if (weekStartsOn === 1) {
    return [...localizedDayNames.slice(1), localizedDayNames[0]];
  } else {
    return localizedDayNames;
  }
};
