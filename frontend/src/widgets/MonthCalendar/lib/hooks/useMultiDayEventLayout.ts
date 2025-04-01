import { useMemo } from 'react';
import {
  isWithinInterval,
  startOfDay,
  endOfDay,
  differenceInDays,
  getDay,
  max,
  min,
} from 'date-fns';
import { CalendarEvent } from '@entities/Event';
import { CalendarDayData } from '@shared/lib/types';

export interface MultiDayEventLayout {
  event: CalendarEvent;
  startCol: number;
  span: number;
  level: number;
  weekIndex: number;
}

const groupCalendarDaysIntoWeeks = (calendarDays: CalendarDayData[]): CalendarDayData[][] => {
  const weeks: CalendarDayData[][] = [];
  const maxDays = Math.min(42, calendarDays.length);
  for (let i = 0; i < maxDays; i += 7) {
    if (i + 7 <= calendarDays.length) {
      const weekSlice = calendarDays.slice(i, i + 7);
      weeks.push(weekSlice);
    } else {
      break;
    }
  }
  return weeks;
};

const sortMultiDayEvents = (events: CalendarEvent[]): CalendarEvent[] => {
  return [...events].sort((a, b) => {
    const startDiff = a.startDate.getTime() - b.startDate.getTime();
    if (startDiff !== 0) return startDiff;

    const durationA = a.endDate ? differenceInDays(a.endDate, a.startDate) : 0;
    const durationB = b.endDate ? differenceInDays(b.endDate, b.startDate) : 0;
    const durationDiff = durationB - durationA;
    if (durationDiff !== 0) return durationDiff;

    return String(a.id).localeCompare(String(b.id));
  });
};

const filterEventsForWeek = (
  events: CalendarEvent[],
  weekStart: Date,
  weekEnd: Date,
): CalendarEvent[] => {
  const weekInterval = { start: weekStart, end: weekEnd };
  return events.filter(
    (event) =>
      isWithinInterval(event.startDate, weekInterval) ||
      (event.endDate && isWithinInterval(event.endDate, weekInterval)) ||
      (event.startDate < weekStart && event.endDate && event.endDate > weekEnd),
  );
};

const calculateLayoutForWeek = (
  week: CalendarDayData[],
  sortedEvents: CalendarEvent[],
  weekIndex: number,
): MultiDayEventLayout[] => {
  const weekLayout: MultiDayEventLayout[] = [];
  if (!week || week.length !== 7) {
    return weekLayout;
  }

  const weekStart = startOfDay(week[0].date);
  const weekEnd = endOfDay(week[6].date);

  const levelOccupancy: Set<number>[] = Array(7)
    .fill(0)
    .map(() => new Set<number>());
  const eventsInWeek = filterEventsForWeek(sortedEvents, weekStart, weekEnd);

  eventsInWeek.forEach((event) => {
    const eventStartInView = max([event.startDate, weekStart]);
    const eventEndInView = event.endDate ? min([event.endDate, weekEnd]) : weekEnd;

    const startDayIndex = getDay(eventStartInView);
    const endDayIndex = getDay(eventEndInView);

    const span = endDayIndex - startDayIndex + 1;

    if (span <= 0) return;

    let level = 0;
    while (true) {
      let levelIsFree = true;
      for (let i = startDayIndex; i <= endDayIndex; i++) {
        if (levelOccupancy[i].has(level)) {
          levelIsFree = false;
          break;
        }
      }
      if (levelIsFree) {
        break;
      }
      level++;
    }

    for (let i = startDayIndex; i <= endDayIndex; i++) {
      levelOccupancy[i].add(level);
    }

    weekLayout.push({
      event,
      startCol: startDayIndex,
      span: span,
      level: level,
      weekIndex: weekIndex,
    });
  });

  return weekLayout;
};

export const useMultiDayEventLayout = (
  multiDayEvents: CalendarEvent[],
  calendarDays: CalendarDayData[],
): MultiDayEventLayout[] => {
  const layout = useMemo((): MultiDayEventLayout[] => {
    if (!calendarDays?.length || !multiDayEvents?.length) {
      return [];
    }

    const weeks = groupCalendarDaysIntoWeeks(calendarDays);
    if (!weeks.length) {
      return [];
    }

    const sortedEvents = sortMultiDayEvents(multiDayEvents);

    const calculatedLayout: MultiDayEventLayout[] = [];
    weeks.forEach((week, weekIndex) => {
      const layoutForWeek = calculateLayoutForWeek(week, sortedEvents, weekIndex);
      calculatedLayout.push(...layoutForWeek);
    });

    return calculatedLayout;
  }, [multiDayEvents, calendarDays]);

  return layout;
};
