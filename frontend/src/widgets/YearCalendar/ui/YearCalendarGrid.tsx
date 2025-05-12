import React, { useMemo } from 'react';
import { Grid } from '@mui/material';
import { getYear, setMonth, startOfYear } from 'date-fns';
import { MiniMonth } from './MiniMonth';
import { CalendarEvent } from '@/entities/Event';

interface YearCalendarGridProps {
  currentDate: Date;
  events: CalendarEvent[];
}

export const YearCalendarGrid: React.FC<YearCalendarGridProps> = React.memo(
  ({ currentDate, events }) => {
    const year = getYear(currentDate);

    const months = useMemo(() => {
      const yearStart = startOfYear(currentDate);
      return Array.from({ length: 12 }, (_, i) => setMonth(yearStart, i));
    }, [currentDate]);

    return (
      <Grid container spacing={1} sx={{ p: { xs: 0.5, sm: 1 }, flexGrow: 1, overflowY: 'auto' }}>
        {months.map((monthDate, index) => (
          <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={index}>
            <MiniMonth monthDate={monthDate} events={events} year={year} />
          </Grid>
        ))}
      </Grid>
    );
  },
);
