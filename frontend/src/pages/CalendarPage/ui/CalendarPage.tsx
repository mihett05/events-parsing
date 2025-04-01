import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { parseISO } from 'date-fns';
import { mockEvents } from '@/shared/lib/mockEvents';

const initialCalendarDate = parseISO('2025-03-01');

export const CalendarPage: React.FC = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Box>
        <MonthCalendar initialDate={initialCalendarDate} events={mockEvents} />
      </Box>
    </Container>
  );
};
