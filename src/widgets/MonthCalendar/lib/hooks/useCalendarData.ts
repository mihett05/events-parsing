import { useMemo } from 'react';
import { CalendarEvent } from '../../../../entities/Event';
import { generateCalendarDays } from '../generateCalendarDays';
import { processEvents } from '../eventUtils';
import { useMultiDayEventLayout } from './useMultiDayEventLayout';
import { MULTI_DAY_EVENT_HEIGHT, MULTI_DAY_EVENT_VERTICAL_GAP } from '../constants';

interface UseCalendarDataProps {
  currentDate: Date;
  events: CalendarEvent[];
}

export const useCalendarData = ({ currentDate, events }: UseCalendarDataProps) => {
  const calendarDays = useMemo(() => generateCalendarDays(currentDate), [currentDate]);

  const { singleDayEventsByDate, multiDayEvents } = useMemo(() => processEvents(events), [events]);

  const multiDayLayout = useMultiDayEventLayout(multiDayEvents, calendarDays);

  const maxLevelsPerWeek = useMemo(() => {
    const levels: number[] = Array(6).fill(-1);
    multiDayLayout.forEach((item) => {
      if (item.weekIndex >= 0 && item.weekIndex < 6) {
        levels[item.weekIndex] = Math.max(levels[item.weekIndex], item.level);
      }
    });
    return levels.map((maxLevel) => (maxLevel > -1 ? maxLevel + 1 : 0));
  }, [multiDayLayout]);

  const spacerHeightsPerWeek = useMemo(() => {
    return maxLevelsPerWeek.map(
      (numLevels) => numLevels * (MULTI_DAY_EVENT_HEIGHT + MULTI_DAY_EVENT_VERTICAL_GAP),
    );
  }, [maxLevelsPerWeek]);

  return {
    calendarDays,
    singleDayEventsByDate,
    multiDayEvents,
    multiDayLayout,
    spacerHeightsPerWeek,
  };
};
