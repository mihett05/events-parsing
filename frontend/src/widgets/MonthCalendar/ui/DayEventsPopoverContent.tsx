import { useMemo } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Divider from '@mui/material/Divider';
import CloseIcon from '@mui/icons-material/Close';
import { format, isValid } from 'date-fns';
import { ru } from 'date-fns/locale';
import { CalendarEvent, EventItem } from '@entities/Event';
import { isEventOnDate } from '@widgets/MonthCalendar/lib/eventUtils';
import { useTranslation } from 'react-i18next';

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
  const { t } = useTranslation();

  if (!date || !isValid(date)) {
    return (
      <Box sx={{ p: 2, minWidth: 200, maxWidth: 300, position: 'relative' }}>
        <Typography variant="caption" color="text.secondary">
          {t('calendar.loading')}
        </Typography>
        <IconButton
          size="small"
          onClick={onClose}
          title={t('calendar.closePopover')}
          sx={{ position: 'absolute', top: 8, right: 8 }}
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      </Box>
    );
  }

  const eventsForThisDay = useMemo(() => {
    return events
      .filter((event) => event && isValid(event.startDate) && isEventOnDate(event, date))
      .sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
  }, [events, date]);

  const formattedDate = format(date, 'EEEE, d MMMM', { locale: ru });

  return (
    <Box sx={{ p: 2, minWidth: 250, maxWidth: 350 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1.5}>
        <Typography variant="subtitle1" fontWeight="bold" id="day-popover-title">
          {formattedDate}
        </Typography>
        <IconButton size="small" onClick={onClose} title={t('calendar.closePopover')}>
          <CloseIcon fontSize="small" />
        </IconButton>
      </Stack>
      <Divider sx={{ mb: 1.5 }} />
      <Stack
        spacing={0.5}
        sx={{
          maxHeight: 300,
          overflowY: 'auto',
          '&::-webkit-scrollbar': { width: '6px' },
          '&::-webkit-scrollbar-track': { background: '#f1f1f1', borderRadius: '3px' },
          '&::-webkit-scrollbar-thumb': { background: '#ccc', borderRadius: '3px' },
          '&::-webkit-scrollbar-thumb:hover': { background: '#aaa' },
          pr: 0.5,
        }}
      >
        {eventsForThisDay.length > 0 ? (
          eventsForThisDay.map((event) => <EventItem key={event.id} event={event} />)
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
            {t('calendar.noEvents')}
          </Typography>
        )}
      </Stack>
    </Box>
  );
};
