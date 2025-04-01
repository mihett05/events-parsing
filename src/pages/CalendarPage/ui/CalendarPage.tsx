import React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { CalendarEvent } from '@entities/Event';
import { parseISO } from 'date-fns';

const mockEvents: CalendarEvent[] = [
  { id: 1, startDate: parseISO('2025-03-11'), title: 'Check-In in Hotel', color: 'orange' },
  {
    id: 2,
    startDate: parseISO('2025-03-11'),
    title: 'Relax and official arrival beer',
    color: 'red',
  },
  { id: 3, startDate: parseISO('2025-03-11'), title: 'Dinner', color: 'orange' },
  { id: 201, startDate: parseISO('2025-03-11'), title: 'Hi', color: 'blue' },
  { id: 202, startDate: parseISO('2025-03-11'), title: 'My name is', color: 'blue' },
  { id: 203, startDate: parseISO('2025-03-11'), title: 'Slim shady', color: 'blue' },
  { id: 4, startDate: parseISO('2025-03-12'), title: 'Breakfast', color: 'orange' },
  { id: 5, startDate: parseISO('2025-03-12'), title: 'Lunch', color: 'orange' },
  { id: 6, startDate: parseISO('2025-03-12'), title: 'Dinner', color: 'orange' },
  { id: 7, startDate: parseISO('2025-03-13'), title: 'Breakfast', color: 'orange' },
  { id: 8, startDate: parseISO('2025-03-13'), title: 'Excursion', color: 'red' },
  { id: 9, startDate: parseISO('2025-03-13'), title: 'Team Building', color: 'green' },
  { id: 10, startDate: parseISO('2025-03-14'), title: 'Breakfast', color: 'orange' },
  { id: 11, startDate: parseISO('2025-03-14'), title: 'Lunch', color: 'orange' },
  { id: 12, startDate: parseISO('2025-03-14'), title: 'Dinner', color: 'orange' },
  { id: 13, startDate: parseISO('2025-03-15'), title: 'Breakfast', color: 'orange' },
  { id: 14, startDate: parseISO('2025-03-15'), title: 'Lunch', color: 'orange' },
  {
    id: 15,
    startDate: parseISO('2025-03-15'),
    title: 'SplitJS conference: Monitoring and...',
    color: 'red',
  },
  { id: 16, startDate: parseISO('2025-03-16'), title: 'Breakfast', color: 'orange' },
  { id: 17, startDate: parseISO('2025-03-16'), title: 'Lunch', color: 'orange' },
  { id: 18, startDate: parseISO('2025-03-16'), title: 'Dinner', color: 'orange' },
  {
    id: 100,
    startDate: parseISO('2025-03-11'),
    endDate: parseISO('2025-03-17'),
    title: 'Hackathon 2025',
    color: 'lightGreen',
    isMultiDay: true,
  },
  {
    id: 101,
    startDate: parseISO('2025-03-18'),
    endDate: parseISO('2025-03-18'),
    title: 'Hackathon 2025',
    color: 'lightGreen',
    isMultiDay: true,
  },
  {
    id: 102,
    startDate: parseISO('2025-03-08'),
    endDate: parseISO('2025-03-12'),
    title: 'Preparation Week',
    color: 'blue',
    isMultiDay: true,
  },
  {
    id: 103,
    startDate: parseISO('2025-03-29'),
    endDate: parseISO('2025-11-02'),
    title: 'Wrap Up Phase',
    color: 'red',
    isMultiDay: true,
  },
  {
    id: 104,
    startDate: parseISO('2025-03-12'),
    endDate: parseISO('2025-03-13'),
    title: 'Mini Sprint',
    color: 'orange',
    isMultiDay: true,
  },
];

const initialCalendarDate = parseISO('2025-03-01');

export const CalendarPage: React.FC = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Box>
        <MonthCalendar initialDate={initialCalendarDate} events={mockEvents} />
      </Box>
    </Container>
  );
};
