import { useMemo } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Divider from '@mui/material/Divider';
import CloseIcon from '@mui/icons-material/Close';
import { format, isValid } from 'date-fns';
import { CalendarEvent, EventItem } from '@entities/Event';
import { isEventOnDate } from '@widgets/MonthCalendar/lib/eventUtils';

interface DayEventsPopoverContentProps {
  date: Date | null;
  events: CalendarEvent[];
  onClose: () => void;
}

export const DayEventsPopoverContent: React.FC<DayEventsPopoverContentProps> = ({
  date,
  events = [],
  onClose,
}) => {
  if (!date || !isValid(date)) {
    return (
      <Box sx={{ p: 2, minWidth: 200, maxWidth: 300 }}>
        <Typography variant="caption" color="text.secondary">
          Loading...
        </Typography>
        <IconButton
          size="small"
          onClick={onClose}
          aria-label="close"
          sx={{ position: 'absolute', top: 8, right: 8 }}
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      </Box>
    );
  }

  const eventsForThisDay = useMemo(() => {
    return events
      .filter((event) => isEventOnDate(event, date))
      .sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
  }, [events]);

  const formattedDate = format(date, 'EEEE, MMM d');

  return (
    <Box sx={{ p: 2, minWidth: 250, maxWidth: 350 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
        <Typography variant="subtitle1" fontWeight="bold" id="day-popover-title">
          {formattedDate}
        </Typography>
        <IconButton
          size="small"
          onClick={onClose}
          aria-label="Close day events popover"
          title="Close"
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      </Stack>
      <Divider sx={{ mb: 1.5 }} />

      <Stack
        spacing={0.5}
        sx={{
          maxHeight: 300,
          overflowY: 'auto',
          pr: 0.5,
        }}
        aria-labelledby="day-popover-title"
      >
        {eventsForThisDay.length > 0 ? (
          eventsForThisDay.map((event) => <EventItem key={event.id} event={event} />)
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
            No events scheduled for this day.
          </Typography>
        )}
      </Stack>
    </Box>
  );
};
