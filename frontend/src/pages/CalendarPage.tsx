import Box from '@mui/material/Box';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { CircularProgress, Typography } from '@mui/material';
import { ApiEvent, formatEvents } from '@/shared/lib/formatEvents';
import { Layout } from '@/shared/ui/Layout';
import { useReadAllEventsV1EventsCalendarGetQuery } from '@/shared/api/api';
import { addMonths, subMonths } from 'date-fns';
import { useAppDispatch, useAppSelector } from '@/shared/store/hooks';
import { setSelectedDate } from '@/features/events/slice';

export const CalendarPage: React.FC = () => {
  const selectedDate = useAppSelector((state) => state.events.selectedDate);
  const dispatch = useAppDispatch();

  const dateWithoutTime = selectedDate;
  dateWithoutTime.setUTCHours(0, 0, 0, 0);

  const startDate = subMonths(dateWithoutTime, 1).toISOString();
  const endDate = addMonths(dateWithoutTime, 1).toISOString();

  const handleMonthChange = (newDate: Date) => {
    const utcDate = new Date(newDate);
    utcDate.setUTCHours(0, 0, 0, 0);
    dispatch(setSelectedDate(utcDate));
  };

  const {
    data: apiEvents,
    error,
    isLoading,
  } = useReadAllEventsV1EventsCalendarGetQuery({ startDate, endDate });

  console.error(error);

  if (isLoading) {
    return (
      <Layout>
        <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
          <CircularProgress />
        </Box>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <Typography color="error" align="center">
          Failed to load events. Please try again later.
        </Typography>
      </Layout>
    );
  }

  const formattedEvents = formatEvents((apiEvents as ApiEvent[]) ?? []);

  return (
    <Layout>
      <MonthCalendar
        initialDate={selectedDate}
        events={formattedEvents}
        onMonthChange={handleMonthChange}
      />
    </Layout>
  );
};
