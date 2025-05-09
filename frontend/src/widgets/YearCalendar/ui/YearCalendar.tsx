import React from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { useCalendarViewData } from '@/features/events/hooks/useCalendarViewData';
import { YearCalendarHeader } from './YearCalendarHeader';
import { YearCalendarGrid } from './YearCalendarGrid';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { useAppDispatch, useAppSelector } from '@/shared/store/hooks';
import {
  CalendarView,
  selectFilteredCalendarEvents,
  setCalendarView,
} from '@/features/events/slice';

export const YearCalendar: React.FC = () => {
  const dispatch = useAppDispatch();
  const { currentDate, isLoading, error, calendarView, handlePrev, handleNext, handleToday } =
    useCalendarViewData();
  const events = useAppSelector(selectFilteredCalendarEvents);

  const handleViewChange = (newView: CalendarView) => {
    dispatch(setCalendarView(newView));
  };

  if (isLoading && events.length === 0) {
    return <LoadingIndicator />;
  }

  if (error && events.length === 0) {
    return <ErrorMessage {...error} />;
  }

  return (
    <Paper
      elevation={0}
      sx={{
        p: { xs: 0, sm: 1 },
        maxWidth: '100%',
        border: '1px solid #eee',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        minHeight: { xs: '70vh', sm: '75vh' },
        position: 'relative',
      }}
    >
      {error && (
        <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, zIndex: 10, p: 1 }}>
          <Paper elevation={2} sx={{ p: 1, bgcolor: 'error.light', color: 'error.contrastText' }}>
            <Typography variant="caption">{error}</Typography>
          </Paper>
        </Box>
      )}
      <YearCalendarHeader
        currentDate={currentDate}
        currentView={calendarView}
        onPrev={handlePrev}
        onNext={handleNext}
        onToday={handleToday}
        onViewChange={handleViewChange}
      />
      <YearCalendarGrid currentDate={currentDate} events={events} />
    </Paper>
  );
};
