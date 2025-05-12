import { EventModel } from '@shared/api/api';
import { CalendarEvent } from './types';
import { differenceInDays, parseISO, isValid } from 'date-fns';

const EVENT_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#8D6FD1', '#D4A5A5'];

export const mapEventToCalendarEvent = (event: EventModel): CalendarEvent | null => {
  const start = parseISO(event.startDate);
  const end = event.endDate ? parseISO(event.endDate) : undefined;
  const endRegistration = event.endRegistration ? parseISO(event.endRegistration) : undefined;

  if (!isValid(start) || (end && !isValid(end)) || (endRegistration && !isValid(endRegistration))) {
    console.error('Invalid date format received from API, skipping event:', event);
    return null;
  }

  const newEvent: CalendarEvent = {
    id: event.id,
    title: event.title,
    startDate: start,
    endDate: end,
    isMultiDay: end ? Math.abs(differenceInDays(start, end)) > 0 : false,
    description: event.description || '',
    type: event.type,
    format: event.format,
    color: EVENT_COLORS[event.id % EVENT_COLORS.length],
    endRegistration: endRegistration,
    organizationId: event.organizationId === undefined ? null : event.organizationId,
  };

  return newEvent;
};
