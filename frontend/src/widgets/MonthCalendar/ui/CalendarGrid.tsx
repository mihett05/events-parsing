import React from 'react';
import Grid from '@mui/material/Grid';
import { CalendarDayData } from '@shared/lib/types';
import { CalendarEvent } from '@entities/Event';
import { CalendarDay } from './CalendarDay';

interface CalendarGridProps {
  calendarDays: CalendarDayData[];
  events: CalendarEvent[];
  onDayClick: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
}

export const CalendarGrid: React.FC<CalendarGridProps> = ({ calendarDays, events, onDayClick }) => {
  return (
    <Grid
      container
      columns={7}
      sx={{
        borderLeft: '1px solid #eee',
        borderTop: '1px solid #eee',
        flexGrow: 1,
        position: 'relative',
      }}
    >
      {calendarDays.map((dayData, index) => {
        const key =
          dayData.date instanceof Date && !isNaN(dayData.date.valueOf())
            ? dayData.date.toISOString()
            : `day-${index}`;

        return (
          <Grid size={1} key={key}>
            <CalendarDay dayData={dayData} events={events} onDayClick={onDayClick} />
          </Grid>
        );
      })}
    </Grid>
  );
};
