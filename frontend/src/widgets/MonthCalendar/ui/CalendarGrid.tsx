import { CalendarDayData } from '@shared/lib/types';
import { CalendarEvent } from '@entities/Event';
import { CalendarDay } from './CalendarDay';
import { isValid } from 'date-fns';
import { Grid } from '@mui/system';

interface CalendarGridProps {
  calendarDays: CalendarDayData[];
  events: CalendarEvent[];
  onDayClick: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
}

export const CalendarGrid: React.FC<CalendarGridProps> = ({ calendarDays, events, onDayClick }) => {
  return (
    <Grid
      container
      columns={7}
      sx={{
        borderLeft: '1px solid #eee',
        borderTop: '1px solid #eee',
        flexGrow: 1,
        position: 'relative',
      }}
      role="grid"
    >
      {calendarDays.map((dayData, index) => {
        const key =
          dayData?.date && isValid(dayData.date)
            ? dayData.date.toISOString()
            : `invalid-day-${index}`;

        return (
          <Grid key={key} size={1}>
            <CalendarDay dayData={dayData} events={events} onDayClick={onDayClick} />
          </Grid>
        );
      })}
    </Grid>
  );
};
