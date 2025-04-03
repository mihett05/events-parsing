import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Divider from '@mui/material/Divider';
import CloseIcon from '@mui/icons-material/Close';
import { format } from 'date-fns';
import { CalendarEvent, EventItem } from '@entities/Event';
import { useTheme } from '@mui/material/styles';
import { getEventBackgroundColor } from '@widgets/MonthCalendar/lib/eventUtils';
import { useModalContext } from '../../lib/hooks/useModalContext';

interface DayEventsPopoverContentProps {
  date: Date;
  singleEvents: CalendarEvent[];
  multiDayEvents: CalendarEvent[];
  onClose: () => void;
}

export const DayEventsPopoverContent: React.FC<DayEventsPopoverContentProps> = ({
  date,
  singleEvents,
  multiDayEvents,
  onClose,
}) => {
  const theme = useTheme();
  const { setSelectedEvent } = useModalContext();

  return (
    <Box sx={{ p: 2, minWidth: 250, maxWidth: 350 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
        <Typography variant="subtitle1" fontWeight="bold">
          {format(date, 'EEEE, MMM d')}
        </Typography>
        <IconButton size="small" onClick={onClose} aria-label="close">
          <CloseIcon fontSize="small" />
        </IconButton>
      </Stack>
      <Divider sx={{ mb: 1.5 }} />

      <Stack spacing={0.5} sx={{ maxHeight: 300, overflowY: 'auto', cursor: 'pointer' }}>
        {multiDayEvents.map((event) => (
          <Box
            key={`pop-${event.id}`}
            onClick={() => setSelectedEvent(event)}
            sx={{
              backgroundColor: getEventBackgroundColor(event),
              color: theme.palette.getContrastText(getEventBackgroundColor(event)),
              borderRadius: '4px',
              p: '2px 8px',
              mb: '4px',
              fontSize: '0.75rem',
              overflow: 'hidden',
              whiteSpace: 'nowrap',
              textOverflow: 'ellipsis',
            }}
          >
            {event.title}
          </Box>
        ))}

        {singleEvents.map((event) => (
          <EventItem key={event.id} event={event} />
        ))}

        {multiDayEvents.length === 0 && singleEvents.length === 0 && (
          <Typography variant="body2" color="text.secondary">
            No events for this day.
          </Typography>
        )}
      </Stack>
    </Box>
  );
};
