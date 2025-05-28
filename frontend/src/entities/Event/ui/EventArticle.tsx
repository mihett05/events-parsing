import React from 'react';
import { Box, Chip, Typography, Paper, Grid, Stack, Divider, Button } from '@mui/material';
import { CalendarEvent } from '../model/types';
import { format, isValid, isSameDay, Locale } from 'date-fns';
import { ru } from 'date-fns/locale';
import { useTranslation } from 'react-i18next';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import EventIcon from '@mui/icons-material/Event';
import EditCalendarIcon from '@mui/icons-material/EditCalendar';
import {
  useReadSubscribersV1EventsSubscribeEventIdGetQuery,
  useSubscribeV1EventsSubscribeEventIdPostMutation,
  useUnsubscribeV1EventsSubscribeEventIdDeleteMutation,
} from '@/shared/api/api';
import { useAppSelector } from '@/shared/store/hooks';

type EventArticleProps = {
  event: CalendarEvent;
};

const InfoRow: React.FC<{ icon: React.ReactNode; label: string; value: React.ReactNode }> = ({
  icon,
  label,
  value,
}) => (
  <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 0.5 }}>
    {React.cloneElement(icon as React.ReactElement, {
      sx: { fontSize: '1.1rem', color: 'text.secondary' },
    })}
    <Typography variant="body2" component="span" sx={{ color: 'text.secondary', minWidth: 60 }}>
      {label}:
    </Typography>
    <Typography variant="body2" component="span" sx={{ fontWeight: 500 }}>
      {value}
    </Typography>
  </Stack>
);

export const EventArticle = React.forwardRef<HTMLDivElement, EventArticleProps>(
  ({ event }, ref) => {
    const { t } = useTranslation();

    const formatDateSafe = (
      date: Date | undefined,
      formatString: string = 'PPP',
      options: { locale?: Locale } = { locale: ru },
    ): string => {
      return date && isValid(date) ? format(date, formatString, options) : 'N/A';
    };

    const formattedStartDate = formatDateSafe(event.startDate);
    const formattedStartTime = formatDateSafe(event.startDate, 'p');
    const formattedEndDate = formatDateSafe(event.endDate);
    const formattedEndTime = formatDateSafe(event.endDate, 'p');
    const formattedEndRegistration = formatDateSafe(event.endRegistration);

    const isSingleDayEvent = !event.endDate || isSameDay(event.startDate, event.endDate);

    const user = useAppSelector((state) => state.user.user);

    const subscribers = useReadSubscribersV1EventsSubscribeEventIdGetQuery({
      eventId: event.id,
    });

    const [subscribe, subscribeMutation] = useSubscribeV1EventsSubscribeEventIdPostMutation();
    const [unsubscribe] = useUnsubscribeV1EventsSubscribeEventIdDeleteMutation();

    const isSubscribed =
      !subscribers.isLoading && subscribers.data?.filter((u) => u.id === user?.id).length;

    return (
      <Paper
        ref={ref}
        elevation={1}
        variant="outlined"
        sx={{
          p: { xs: 2, sm: 3 },
          borderRadius: 2,
          position: 'relative',
          overflow: 'hidden',
          borderLeft: `5px solid ${event.color}`,
        }}
      >
        <Stack spacing={2}>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="h6" component="h3" fontWeight="bold" gutterBottom sx={{ mb: 0 }}>
              {event.title}
            </Typography>
            <Button
              variant="outlined"
              size="small"
              disabled={user === null}
              color={isSubscribed ? 'error' : 'primary'}
              onClick={async () => {
                if (!isSubscribed) {
                  await subscribe({
                    eventId: event.id,
                  }).unwrap();
                } else {
                  await unsubscribe({
                    eventId: event.id,
                  }).unwrap();
                }
                subscribers.refetch();
              }}
            >
              {isSubscribed ? 'Отписаться' : 'Подписаться'}
            </Button>
          </Box>
          <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap">
            <Chip
              icon={<EventIcon fontSize="small" />}
              label={event.type}
              size="small"
              variant="outlined"
              sx={{ borderColor: event.color, color: event.color }}
            />
            <Chip label={event.format} size="small" variant="outlined" />
          </Stack>
          <Divider />
          <Grid container spacing={1.5}>
            <Grid size={{ xs: 12, sm: isSingleDayEvent ? 12 : 6 }}>
              <InfoRow
                icon={<CalendarTodayIcon />}
                label={t('event.start')}
                value={`${formattedStartDate}, ${formattedStartTime}`}
              />
            </Grid>
            {!isSingleDayEvent && event.endDate && (
              <Grid size={{ xs: 12, sm: 6 }}>
                <InfoRow
                  icon={<AccessTimeIcon />}
                  label={t('event.end')}
                  value={`${formattedEndDate}, ${formattedEndTime}`}
                />
              </Grid>
            )}
            {event.endRegistration && isValid(event.endRegistration) && (
              <Grid size={{ xs: 12 }}>
                <InfoRow
                  icon={<EditCalendarIcon />}
                  label={t('event.registrationUntil', { date: '' }).replace(':', '').trim()}
                  value={formattedEndRegistration}
                />
              </Grid>
            )}
          </Grid>
          {event.description && String(event.description).trim() && (
            <>
              <Divider />
              <Box>
                <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
                  {t('event.description')}:
                </Typography>
                <Typography
                  variant="body2"
                  component="div"
                  sx={{
                    whiteSpace: 'pre-wrap',
                    lineHeight: 1.6,
                    color: 'text.secondary',
                    pl: 1,
                  }}
                >
                  {event.description}
                </Typography>
              </Box>
            </>
          )}
        </Stack>
      </Paper>
    );
  },
);
