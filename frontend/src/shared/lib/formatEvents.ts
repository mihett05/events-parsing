import { CalendarEvent } from '@/entities/Event';
import { differenceInDays } from 'date-fns';

export interface ApiEvent {
  createdAt: string;
  description: string;
  endDate: string;
  endRegistration: string;
  format: string;
  id: number;
  isVisible: boolean;
  startDate: string;
  title: string;
  type: string;
}

export const formatEvents = (events: ApiEvent[]): CalendarEvent[] => {
  const colors = [
    '#FF6B6B', // Красный
    '#4ECDC4', // Бирюзовый
    '#45B7D1', // Голубой
    '#96CEB4', // Мятный
    '#FFEEAD', // Жёлтый
    '#D4A5A5', // Пудровый
  ];
  return events.reduce((accum, value, index) => {
    const start = new Date(value.startDate);
    const end = new Date(value.endDate);

    const newEvent: CalendarEvent = {
      id: value.id,
      title: value.title,
      startDate: start,
      endDate: end,
      isMultiDay: Math.abs(differenceInDays(start, end)) > 0,
      description: value.description,
      type: value.type,
      format: value.format,
      color: colors[index % colors.length],
    };

    accum.push(newEvent);
    return accum;
  }, [] as CalendarEvent[]);
};
