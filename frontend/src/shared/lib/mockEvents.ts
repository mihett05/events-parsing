import { CalendarEvent } from '@/entities/Event';
import { parseISO } from 'date-fns';

export const mockEvents: CalendarEvent[] = [
  {
    id: 1,
    startDate: parseISO('2025-03-11'),
    title: 'Check-In in Hotel',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 2,
    startDate: parseISO('2025-03-11'),
    title: 'Relax and official arrival beer',
    color: 'red',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 3,
    startDate: parseISO('2025-03-11'),
    title: 'Dinner',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus. \
      Ab, praesentium blanditiis! Velit sequi, quaerat commodi dolorem voluptas fuga tenetur sint. Et, aliquid?',
    type: 'other',
    format: 'offline',
  },
  {
    id: 201,
    startDate: parseISO('2025-03-11'),
    title: 'Hi',
    color: 'blue',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus. \
      Ab, praesentium blanditiis! Velit sequi, quaerat commodi dolorem voluptas fuga tenetur sint. Et, aliquid?',
    type: 'other',
    format: 'hybrid',
  },
  {
    id: 202,
    startDate: parseISO('2025-03-11'),
    title: 'My name is',
    color: 'blue',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'online',
  },
  {
    id: 203,
    startDate: parseISO('2025-03-11'),
    title: 'Slim shady',
    color: 'blue',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 4,
    startDate: parseISO('2025-03-12'),
    title: 'Breakfast',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 5,
    startDate: parseISO('2025-03-12'),
    title: 'Lunch',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 6,
    startDate: parseISO('2025-03-12'),
    title: 'Dinner',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 7,
    startDate: parseISO('2025-03-13'),
    title: 'Breakfast',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 8,
    startDate: parseISO('2025-03-13'),
    title: 'Excursion',
    color: 'red',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 9,
    startDate: parseISO('2025-03-13'),
    title: 'Team Building',
    color: 'green',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'online',
  },
  {
    id: 10,
    startDate: parseISO('2025-03-14'),
    title: 'Breakfast',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 11,
    startDate: parseISO('2025-03-14'),
    title: 'Lunch',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 12,
    startDate: parseISO('2025-03-14'),
    title: 'Dinner',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 13,
    startDate: parseISO('2025-03-15'),
    title: 'Breakfast',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 14,
    startDate: parseISO('2025-03-15'),
    title: 'Lunch',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 15,
    startDate: parseISO('2025-03-15'),
    title: 'SplitJS conference: Monitoring and...',
    color: 'red',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'conference',
    format: 'online',
  },
  {
    id: 16,
    startDate: parseISO('2025-03-16'),
    title: 'Breakfast',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 17,
    startDate: parseISO('2025-03-16'),
    title: 'Lunch',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 18,
    startDate: parseISO('2025-03-16'),
    title: 'Dinner',
    color: 'orange',
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'other',
    format: 'offline',
  },
  {
    id: 100,
    startDate: parseISO('2025-03-11'),
    endDate: parseISO('2025-03-17'),
    title: 'Hackathon 2025',
    color: 'lightGreen',
    isMultiDay: true,
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'hackaton',
    format: 'online',
  },
  {
    id: 101,
    startDate: parseISO('2025-03-18'),
    endDate: parseISO('2025-03-18'),
    title: 'Hackathon 2025',
    color: 'lightGreen',
    isMultiDay: true,
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'hackaton',
    format: 'online',
  },
  {
    id: 102,
    startDate: parseISO('2025-03-08'),
    endDate: parseISO('2025-03-12'),
    title: 'Preparation Week',
    color: 'blue',
    isMultiDay: true,
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'hackaton',
    format: 'online',
  },
  {
    id: 103,
    startDate: parseISO('2025-03-29'),
    endDate: parseISO('2025-05-02'),
    title: 'Wrap Up Phase',
    color: 'red',
    isMultiDay: true,
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'hackaton',
    format: 'online',
  },
  {
    id: 104,
    startDate: parseISO('2025-03-12'),
    endDate: parseISO('2025-03-13'),
    title: 'Mini Sprint',
    color: 'orange',
    isMultiDay: true,
    description:
      'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio explicabo officiis unde voluptate ea maiores repellendus.',
    type: 'hackaton',
    format: 'online',
  },
];
