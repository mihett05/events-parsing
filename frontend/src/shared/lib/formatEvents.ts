import { CalendarEvent } from '@/entities/Event';
import { differenceInDays } from 'date-fns';

export interface ApiEvent {
  createdAt: string;
  description: string;
  endDate: string;
  endRegistration: string;
  id: number;
  isVisible: boolean;
  startDate: string;
  title: string;
}

export const formatEvents = (events: ApiEvent[]): CalendarEvent[] => {
  const typePossible = ['hackaton', 'Blah-blah-blah', 'Olympiad'];
  const formatPossible = ['online', 'offline', 'hybrid'];
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
      type: typePossible[Math.floor(Math.random() * typePossible.length)],
      format: formatPossible[Math.floor(Math.random() * formatPossible.length)],
      color: colors[index % colors.length],
    };

    accum.push(newEvent);
    return accum;
  }, [] as CalendarEvent[]);
};
