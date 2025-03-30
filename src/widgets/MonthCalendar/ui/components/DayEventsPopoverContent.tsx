import React from 'react';
import { Box, Typography, Stack, IconButton, Divider } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { format } from 'date-fns';
import { CalendarEvent, EventItem } from '../../../../entities/Event';
import { useTheme } from '@mui/material/styles';
import { getEventBackgroundColor } from '../../lib/eventUtils';

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

  return (
    <Box sx={{ p: 2, minWidth: 250, maxWidth: 350 }}>
      {/* Header */}
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
        <Typography variant="subtitle1" fontWeight="bold">
          {format(date, 'EEEE, MMM d')}
        </Typography>
        <IconButton size="small" onClick={onClose} aria-label="close">
          <CloseIcon fontSize="small" />
        </IconButton>
      </Stack>
      <Divider sx={{ mb: 1.5 }} />

      <Stack spacing={0.5} sx={{ maxHeight: 300, overflowY: 'auto' }}>
        {multiDayEvents.map((event) => (
          <Box
            key={`pop-${event.id}`}
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
