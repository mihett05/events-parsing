import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { useReadAllEventsV1EventsGetQuery } from '@/shared/api/api';
import { CircularProgress, Typography } from '@mui/material';
import { ApiEvent, formatEvents } from '@/shared/lib/formatEvents';

const initialCalendarDate = new Date();

export const CalendarPage: React.FC = () => {
  const {
    data: apiEvents,
    error,
    isLoading,
  } = useReadAllEventsV1EventsGetQuery({ page: 0, pageSize: 100000 });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Typography color="error" align="center">
          Failed to load events. Please try again later.
        </Typography>
      </Container>
    );
  }

  const formattedEvents = formatEvents((apiEvents as ApiEvent[]) ?? []);

  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Box>
        <MonthCalendar initialDate={initialCalendarDate} events={formattedEvents} />
      </Box>
    </Container>
  );
};
