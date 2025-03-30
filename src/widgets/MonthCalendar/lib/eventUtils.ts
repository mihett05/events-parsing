import { format, isSameDay, startOfDay } from 'date-fns';
import { CalendarEvent } from '../../../entities/Event';

interface ProcessedEvents {
  singleDayEventsByDate: Record<string, CalendarEvent[]>;
  multiDayEvents: CalendarEvent[];
}

export const processEvents = (events: CalendarEvent[]): ProcessedEvents => {
  const singleDayGrouped: Record<string, CalendarEvent[]> = {};
  const multi: CalendarEvent[] = [];

  events.forEach((event) => {
    const start = startOfDay(event.startDate);
    const end = event.endDate ? startOfDay(event.endDate) : start;

    const isSingle = !event.endDate || isSameDay(start, end) || event.isMultiDay === false;
    const isMulti = !isSingle && event.isMultiDay !== false;

    if (isSingle) {
      const dateKey = format(start, 'yyyy-MM-dd');
      if (!singleDayGrouped[dateKey]) {
        singleDayGrouped[dateKey] = [];
      }
      singleDayGrouped[dateKey].push({ ...event, startDate: start });
    } else if (isMulti) {
      multi.push({ ...event, startDate: start, endDate: end });
    }
  });

  return { singleDayEventsByDate: singleDayGrouped, multiDayEvents: multi };
};

const eventColorMapping: { [key: string]: string } = {
  orange: '#ff9800',
  red: '#f44336',
  green: '#4caf50',
  blue: '#2196f3',
  lightgreen: '#69f0ae',
};

export const getEventBackgroundColor = (event: CalendarEvent): string => {
  return eventColorMapping[event.color.toLowerCase()] || event.color;
};
