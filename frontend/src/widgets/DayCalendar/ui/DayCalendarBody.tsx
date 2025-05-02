import React, { useMemo } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import { EventArticle, CalendarEvent } from '@/entities/Event';
import { isValid } from 'date-fns';
import { useTranslation } from 'react-i18next';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { isEventOnDate } from '@/widgets/MonthCalendar/lib/eventUtils';

interface DayCalendarBodyProps {
  currentDate: Date;
  events: CalendarEvent[];
  isLoading: boolean;
}

export const DayCalendarBody: React.FC<DayCalendarBodyProps> = React.memo(
  ({ currentDate, events, isLoading }) => {
    const { t } = useTranslation();

    const eventsForThisDay = useMemo(() => {
      if (!isValid(currentDate)) return [];
      return events
        .filter((event) => event && isEventOnDate(event, currentDate))
        .sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
    }, [events, currentDate]);

    if (isLoading) {
      return <LoadingIndicator />;
    }

    if (eventsForThisDay.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', p: 3, color: 'text.secondary' }}>
          <Typography>{t('dayView.noEvents')}</Typography>
        </Box>
      );
    }

    return (
      <Stack
        spacing={0}
        gap={3}
        sx={{ p: { xs: 1, sm: 2, md: 3 }, flexGrow: 1, overflowY: 'auto' }}
      >
        {eventsForThisDay.map((event, index) => (
          <React.Fragment key={event.id}>
            <EventArticle event={event} />
            {index < eventsForThisDay.length - 1 && <Divider sx={{ my: 2 }} />}
          </React.Fragment>
        ))}
      </Stack>
    );
  },
);
