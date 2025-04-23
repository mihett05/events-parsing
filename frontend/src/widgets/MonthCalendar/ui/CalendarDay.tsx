import React, { useMemo } from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { format, isToday as isTodayDateFns, isValid } from 'date-fns';
import { CalendarDayData } from '@shared/lib/types';
import { CalendarEvent, EventItem } from '@entities/Event';
import { isEventOnDate } from '@widgets/MonthCalendar/lib/eventUtils';
import { DATE_NUMBER_AREA_HEIGHT } from '@widgets/MonthCalendar/lib/constants';
import { SxProps } from '@mui/material';

const MAX_VISIBLE_EVENTS_IN_CELL = 2;
const FIXED_CELL_HEIGHT_NUMERIC = 120;
const FIXED_CELL_HEIGHT = `${FIXED_CELL_HEIGHT_NUMERIC}px`;

interface CalendarDayProps {
  dayData: CalendarDayData;
  events: CalendarEvent[];
  onDayClick: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
}

export const CalendarDay: React.FC<CalendarDayProps> = React.memo(
  ({ dayData, events, onDayClick }) => {
    if (!dayData || !dayData.date || !isValid(dayData.date)) {
      console.error('CalendarDay received invalid dayData:', dayData);
      return (
        <Box
          sx={{
            height: FIXED_CELL_HEIGHT,
            border: '1px dashed red',
            p: 1,
            fontSize: '0.8rem',
            color: 'red',
            overflow: 'hidden',
          }}
        >
          Invalid Date Data
        </Box>
      );
    }

    const { date, isCurrentMonth, isWeekend } = dayData;
    const isToday = isTodayDateFns(date);
    const dayNumber = format(date, 'd');

    const eventsForThisDay = useMemo(() => {
      const validEvents = events.filter(
        (event) => event && event.startDate && isValid(event.startDate),
      );
      return validEvents
        .filter((event) => isEventOnDate(event, date))
        .sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
    }, [events, date]);

    const visibleEvents = eventsForThisDay.slice(0, MAX_VISIBLE_EVENTS_IN_CELL);
    const hiddenCount = Math.max(0, eventsForThisDay.length - MAX_VISIBLE_EVENTS_IN_CELL);

    const getDayStyles = (): SxProps => ({
      display: 'flex',
      flexDirection: 'column',
      height: FIXED_CELL_HEIGHT,
      borderRight: '1px solid #eee',
      borderBottom: '1px solid #eee',
      cursor: 'pointer',
      transition: 'background-color 0.2s ease',
      backgroundColor: isCurrentMonth ? '#fff' : '#fafafa',
      position: 'relative',
      overflow: 'hidden',
      color: isCurrentMonth ? 'inherit' : '#9e9e9e',
      '&:hover': {
        backgroundColor: isCurrentMonth ? '#f5f5f5' : '#f0f0f0',
      },
    });

    const getNumberStyles = (): SxProps => {
      const styles: React.CSSProperties = {
        width: '24px',
        height: '24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '50%',
        fontSize: '0.8rem',
        fontWeight: isToday ? 'bold' : 'normal',
        color: !isCurrentMonth ? '#bdbdbd' : isWeekend && isCurrentMonth ? '#d32f2f' : 'inherit',
        marginLeft: 'auto',
        flexShrink: 0,
      };
      if (isToday) {
        styles.backgroundColor = '#1976d2';
        styles.color = '#fff';
      }
      return styles;
    };

    const handleCellClick = (e: React.MouseEvent<HTMLElement>) => {
      onDayClick(e, date);
    };

    return (
      <Box
        sx={getDayStyles()}
        onClick={handleCellClick}
        title={`Click to see events for ${format(date, 'MMM d')}`}
      >
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            p: '4px',
            height: `${DATE_NUMBER_AREA_HEIGHT}px`,
            boxSizing: 'border-box',
            flexShrink: 0,
          }}
        >
          <Typography variant="body2" component="div" sx={getNumberStyles()}>
            {dayNumber}
          </Typography>
        </Box>

        <Stack
          spacing={0.2}
          sx={{
            width: '100%',
            px: '4px',
            pb: '2px',
            flexGrow: 1,
            overflow: 'hidden',
            justifyContent: 'flex-start',
          }}
        >
          {visibleEvents.map((event) => (
            <EventItem key={event.id} event={event} />
          ))}

          {hiddenCount > 0 && (
            <Typography
              variant="caption"
              sx={{
                fontSize: '0.65rem',
                color: 'text.secondary',
                mt: 'auto',
                pt: '2px',
                alignSelf: 'flex-start',
                pl: '2px',
                pointerEvents: 'none',
              }}
            >
              +{hiddenCount} more
            </Typography>
          )}
        </Stack>
      </Box>
    );
  },
);
