import React from 'react';
import Grid from '@mui/material/Grid';
import { CalendarDayData } from '@shared/lib/types';
import { CalendarEvent } from '@entities/Event';
import { CalendarDay } from './CalendarDay/CalendarDay';
import { format } from 'date-fns';

interface CalendarGridProps {
  calendarDays: CalendarDayData[];
  singleDayEventsByDate: Record<string, CalendarEvent[]>;
  spacerHeightsPerWeek: number[];
  onShowMoreClick: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
}

export const CalendarGrid = React.forwardRef<HTMLDivElement, CalendarGridProps>(
  ({ calendarDays, singleDayEventsByDate, spacerHeightsPerWeek, onShowMoreClick }, ref) => {
    return (
      <Grid
        container
        columns={7}
        ref={ref}
        sx={{
          borderLeft: '1px solid #eee',
          borderTop: '1px solid #eee',
          flexGrow: 1,
          position: 'relative',
        }}
      >
        {calendarDays.map((dayData, index) => {
          const dateKey = format(dayData.date, 'yyyy-MM-dd');
          const singleEventsForDay = singleDayEventsByDate[dateKey] || [];
          const weekIndex = Math.floor(index / 7);
          const multiDaySpacerHeight = spacerHeightsPerWeek[weekIndex] ?? 0;

          return (
            <Grid size={1} key={dayData.date.toISOString()}>
              <CalendarDay
                dayData={dayData}
                singleDayEvents={singleEventsForDay}
                multiDaySpacerHeight={multiDaySpacerHeight}
                onShowMoreClick={onShowMoreClick}
              />
            </Grid>
          );
        })}
      </Grid>
    );
  },
);
