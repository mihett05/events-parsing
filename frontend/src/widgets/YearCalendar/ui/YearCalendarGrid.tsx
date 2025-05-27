import React, { useMemo } from 'react';
import { Box, Grid } from '@mui/material';
import { getYear, setMonth, startOfYear, isValid as isValidDate } from 'date-fns';
import { MiniMonth } from './MiniMonth';
import { CalendarEvent } from '@/entities/Event';

interface YearCalendarGridProps {
  currentDate: Date;
  events: CalendarEvent[];
  onMonthClick: (date: Date) => void;
  onDayClick: (date: Date) => void;
}

export const YearCalendarGrid: React.FC<YearCalendarGridProps> = ({
  currentDate,
  events,
  onMonthClick,
  onDayClick,
}) => {
  const year = getYear(currentDate);

  const months = useMemo(() => {
    if (!isValidDate(currentDate)) return [];
    const yearStart = startOfYear(currentDate);
    return Array.from({ length: 12 }, (_, i) => setMonth(yearStart, i));
  }, [currentDate]);

  if (months.length === 0) {
    return null;
  }

  return (
    <Grid
      container
      spacing={{ xs: 0.5, sm: 1 }}
      sx={{ p: { xs: 0.5, sm: 1 }, flexGrow: 1, overflowY: 'auto' }}
    >
      {months.map((monthDate, index) => (
        <Grid
          size={{ xs: 12, sm: 6, md: 4, lg: 3 }}
          key={isValidDate(monthDate) ? monthDate.toISOString() : index}
        >
          {' '}
          {isValidDate(monthDate) ? (
            <MiniMonth
              monthDate={monthDate}
              events={events}
              year={year}
              onMonthClick={onMonthClick}
              onDayClick={onDayClick}
            />
          ) : (
            <Box sx={{ p: 1, height: '100%', border: '1px dashed grey' }}>Invalid Month Data</Box>
          )}
        </Grid>
      ))}
    </Grid>
  );
};
