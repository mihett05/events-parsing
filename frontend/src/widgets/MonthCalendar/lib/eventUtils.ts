import { startOfDay, endOfDay, isSameDay, isValid } from 'date-fns';
import { CalendarEvent } from '@entities/Event';

export const isEventOnDate = (event: CalendarEvent, date: Date): boolean => {
  const dayStart = startOfDay(date);
  const dayEnd = endOfDay(date);
  if (!event?.startDate || !isValid(event.startDate)) return false;

  const eventStart = startOfDay(event.startDate);
  if (!isValid(eventStart)) return false;

  if (!event.endDate || isSameDay(eventStart, event.endDate)) {
    return isSameDay(eventStart, dayStart);
  }

  const eventEnd = endOfDay(event.endDate);
  if (!isValid(eventEnd)) return false;

  return eventStart <= dayEnd && eventEnd >= dayStart;
};
