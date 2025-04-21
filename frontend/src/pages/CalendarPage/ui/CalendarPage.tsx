import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { parseISO } from 'date-fns';
import { useReadAllEventsV1EventsGetQuery } from '@/shared/api/api';
import { CircularProgress } from '@mui/material';
import { ApiEvent, formatEvents } from '@/shared/lib/formatEvents';
// import { mockEvents } from '@/shared/lib/mockEvents';

const initialCalendarDate = parseISO(new Date().toISOString());

export const CalendarPage: React.FC = () => {
  const {
    data: events,
    // error,
    isLoading,
  } = useReadAllEventsV1EventsGetQuery({ page: 0, pageSize: 100000 });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Box>
        {/* <MonthCalendar initialDate={initialCalendarDate} events={mockEvents} /> */}
        <MonthCalendar
          initialDate={initialCalendarDate}
          events={formatEvents(events as ApiEvent[])}
        />
      </Box>
    </Container>
  );
};
