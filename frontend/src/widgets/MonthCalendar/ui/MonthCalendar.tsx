import { CalendarHeader } from './CalendarHeader';
import { DayNamesHeader } from './DayNamesHeader';
import { CalendarGrid } from './CalendarGrid';
import { DayEventsPopoverContent } from './DayEventsPopoverContent';
import { isValid } from 'date-fns';
import { Box, Paper, Popover, Typography } from '@mui/material';
import { generateCalendarDays, useDayEventsPopover, useLocalizedDayNames } from '../lib';
import { useCalendarViewData } from '@/features/events/hooks/useCalendarViewData';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { useAppDispatch } from '@/shared/store/hooks';
import { CalendarView, setCalendarView } from '@/features/events/slice';

export const MonthCalendar: React.FC = () => {
  const dispatch = useAppDispatch();
  const {
    events,
    isLoading,
    error,
    currentDate,
    calendarView,
    handlePrev,
    handleNext,
    handleToday,
  } = useCalendarViewData();

  const {
    popoverId,
    isPopoverOpen,
    popoverAnchorEl,
    selectedDateForPopover,
    openPopover,
    closePopover,
  } = useDayEventsPopover();

  const dayNames = useLocalizedDayNames(1);
  const calendarDays = generateCalendarDays(currentDate, 1);

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
        p: { xs: 0.5, sm: 1 },
        maxWidth: '100%',
        border: '1px solid #eee',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        minHeight: '75vh',
        position: 'relative',
      }}
    >
      {error && (
        <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, zIndex: 10, p: 1 }}>
          <Paper elevation={2} sx={{ p: 1, bgcolor: 'error.light', color: 'error.contrastText' }}>
            <Typography variant="caption">{error.messageKey}</Typography>
          </Paper>
        </Box>
      )}
      <CalendarHeader
        currentDate={currentDate}
        currentView={calendarView}
        onPrev={handlePrev}
        onNext={handleNext}
        onToday={handleToday}
        onViewChange={handleViewChange}
      />
      <Box
        sx={{
          position: 'relative',
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        <DayNamesHeader dayNames={dayNames} />
        <CalendarGrid calendarDays={calendarDays} events={events} onDayClick={openPopover} />
      </Box>
      <Popover
        id={popoverId}
        open={isPopoverOpen}
        anchorEl={popoverAnchorEl}
        onClose={closePopover}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        transformOrigin={{ vertical: 'top', horizontal: 'center' }}
        slotProps={{
          paper: {
            sx: {
              boxShadow: '0px 5px 15px rgba(0,0,0,0.2)',
              borderRadius: '8px',
              mt: 0.5,
            },
          },
        }}
        disableRestoreFocus
      >
        {isPopoverOpen && selectedDateForPopover && isValid(selectedDateForPopover) && (
          <DayEventsPopoverContent
            date={selectedDateForPopover}
            events={events}
            onClose={closePopover}
          />
        )}
      </Popover>
    </Paper>
  );
};
