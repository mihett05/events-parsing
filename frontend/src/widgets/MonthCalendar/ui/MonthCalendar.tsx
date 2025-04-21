import { useMemo, useState, useCallback } from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Popover from '@mui/material/Popover';
import { CalendarEvent } from '@entities/Event';
import { getDayNames, useCalendarNavigation, generateCalendarDays } from '../lib';
import { CalendarHeader } from './CalendarHeader';
import { DayNamesHeader } from './DayNamesHeader';
import { CalendarGrid } from './CalendarGrid';
import { DayEventsPopoverContent } from './DayEventsPopoverContent';
import { EventDetailsModal } from './EventDetailsModal';
import { ModalProvider } from '../lib/context/ModalContext';
import { isValid } from 'date-fns';

interface MonthCalendarProps {
  events?: CalendarEvent[];
  initialDate?: Date;
}

export const MonthCalendar: React.FC<MonthCalendarProps> = ({ events = [], initialDate }) => {
  const { currentDate, handlePrevMonth, handleNextMonth, handleToday } = useCalendarNavigation({
    initialDate,
  });

  const [dayPopoverAnchorEl, setDayPopoverAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedDateForPopover, setSelectedDateForPopover] = useState<null | Date>(null);

  const safeCurrentDate = useMemo(
    () => (isValid(currentDate) ? currentDate : new Date()),
    [currentDate],
  );

  const calendarDays = useMemo(() => {
    return generateCalendarDays(safeCurrentDate);
  }, [safeCurrentDate]);

  const dayNames = useMemo(() => getDayNames(0), []);

  const handleDayClick = useCallback((event: React.MouseEvent<HTMLElement>, date: Date) => {
    if (isValid(date)) {
      setSelectedDateForPopover(date);
      setDayPopoverAnchorEl(event.currentTarget);
    } else {
      console.warn('Attempted to open popover for invalid date:', date);
    }
  }, []);

  const handleDayPopoverClose = useCallback(() => {
    setDayPopoverAnchorEl(null);
  }, []);

  const isDayPopoverOpen = Boolean(dayPopoverAnchorEl);
  const dayPopoverId = isDayPopoverOpen ? 'day-events-popover' : undefined;

  return (
    <ModalProvider>
      <Paper
        elevation={0}
        sx={{
          p: { xs: 0.5, sm: 1 },
          maxWidth: '100%',
          border: '1px solid #eee',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          minHeight: '70vh',
        }}
      >
        <CalendarHeader
          currentDate={safeCurrentDate}
          onPrevMonth={handlePrevMonth}
          onNextMonth={handleNextMonth}
          onToday={handleToday}
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

          <CalendarGrid calendarDays={calendarDays} events={events} onDayClick={handleDayClick} />
        </Box>

        <Popover
          id={dayPopoverId}
          open={isDayPopoverOpen}
          anchorEl={dayPopoverAnchorEl}
          onClose={handleDayPopoverClose}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          transformOrigin={{ vertical: 'top', horizontal: 'center' }}
          slotProps={{
            paper: {
              sx: {
                boxShadow: '0px 4px 12px rgba(0,0,0,0.15)',
                borderRadius: '8px',
              },
            },
          }}
          aria-modal="true"
        >
          <DayEventsPopoverContent
            date={selectedDateForPopover}
            events={events}
            onClose={handleDayPopoverClose}
          />
        </Popover>
        <EventDetailsModal />
      </Paper>
    </ModalProvider>
  );
};
