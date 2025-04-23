import { EventModel } from '@shared/api/api';
import { CalendarEvent } from './types';
import { differenceInDays } from 'date-fns';

export const mapEventToCalendarEvent = (event: EventModel): CalendarEvent => {
  const colors = [
    '#FF6B6B', // Красный
    '#4ECDC4', // Бирюзовый
    '#45B7D1', // Голубой
    '#96CEB4', // Мятный
    '#FFEEAD', // Жёлтый
    '#D4A5A5', // Пудровый
  ];

  const start = new Date(event.startDate);
  const end = event.endDate ? new Date(event.endDate) : undefined;

  const newEvent: CalendarEvent = {
    id: event.id,
    title: event.title,
    startDate: start,
    endDate: end,
    isMultiDay: end ? Math.abs(differenceInDays(start, end)) > 0 : false,
    description: event.description || '',
    type: event.type,
    format: event.format,
    color: colors[event.id % colors.length],
  };

  return newEvent;
};
