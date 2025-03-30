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
import { CalendarEvent } from '../../../../entities/Event';
import { CalendarDayData } from '../../../../shared/lib/types';

export interface MultiDayEventLayout {
  event: CalendarEvent;
  startCol: number;
  span: number;
  level: number;
  weekIndex: number;
}

export const useMultiDayEventLayout = (
  multiDayEvents: CalendarEvent[],
  calendarDays: CalendarDayData[],
): MultiDayEventLayout[] => {
  const layout = useMemo((): MultiDayEventLayout[] => {
    if (!calendarDays.length || !multiDayEvents.length) {
      return [];
    }

    const calculatedLayout: MultiDayEventLayout[] = [];
    const weeks: CalendarDayData[][] = [];
    for (let i = 0; i < 42 && i < calendarDays.length; i += 7) {
      const weekSlice = calendarDays.slice(i, Math.min(i + 7, calendarDays.length));
      if (weekSlice.length === 7) {
        weeks.push(weekSlice);
      }
    }

    const sortedEvents = [...multiDayEvents].sort((a, b) => {
      const startDiff = a.startDate.getTime() - b.startDate.getTime();
      if (startDiff !== 0) return startDiff;
      const durationA = differenceInDays(a.endDate!, a.startDate);
      const durationB = differenceInDays(b.endDate!, b.startDate);
      const durationDiff = durationB - durationA;
      if (durationDiff !== 0) return durationDiff;
      return String(a.id).localeCompare(String(b.id));
    });

    weeks.forEach((week, weekIndex) => {
      const weekStart = startOfDay(week[0].date);
      const weekEnd = endOfDay(week[6].date);
      const weekInterval = { start: weekStart, end: weekEnd };

      const levelOccupancy: Set<number>[] = Array(7)
        .fill(0)
        .map(() => new Set<number>());

      const eventsInWeek = sortedEvents.filter(
        (event) =>
          isWithinInterval(event.startDate, weekInterval) ||
          (event.endDate && isWithinInterval(event.endDate, weekInterval)) ||
          (event.startDate < weekStart && event.endDate && event.endDate > weekEnd),
      );

      eventsInWeek.forEach((event) => {
        const eventStartInView = max([event.startDate, weekStart]);
        const eventEndInView = min([event.endDate!, weekEnd]);

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
          if (levelIsFree) break;
          level++;
        }

        for (let i = startDayIndex; i <= endDayIndex; i++) {
          levelOccupancy[i].add(level);
        }

        calculatedLayout.push({
          event,
          startCol: startDayIndex,
          span: span,
          level: level,
          weekIndex: weekIndex,
        });
      });
    });

    return calculatedLayout;
  }, [multiDayEvents, calendarDays]);

  return layout;
};
