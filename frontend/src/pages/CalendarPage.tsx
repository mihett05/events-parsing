import Box from '@mui/material/Box';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { useReadAllEventsV1EventsGetQuery } from '@/shared/api/api';
import { CircularProgress, Typography } from '@mui/material';
import { ApiEvent, formatEvents } from '@/shared/lib/formatEvents';
import { Layout } from '@/shared/ui/Layout';

const initialCalendarDate = new Date();

export const CalendarPage: React.FC = () => {
  const {
    data: apiEvents,
    error,
    isLoading,
  } = useReadAllEventsV1EventsGetQuery({ page: 0, pageSize: 100000 });

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
      <MonthCalendar initialDate={initialCalendarDate} events={formattedEvents} />
    </Layout>
  );
};
