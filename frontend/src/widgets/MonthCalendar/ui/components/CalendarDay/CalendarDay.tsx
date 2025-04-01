import React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { format, isToday as isTodayDateFns } from 'date-fns';
import { CalendarDayData } from '@shared/lib/types';
import { CalendarEvent, EventItem } from '@entities/Event';
import { DATE_NUMBER_AREA_HEIGHT } from '@widgets/MonthCalendar/lib/constants';
import { calculateVisibleLayout } from './calculateVisibleLayout';

const MAX_VISIBLE_SINGLE_DAY_EVENTS = 3;
const FIXED_CELL_HEIGHT_NUMERIC = 120;
const FIXED_CELL_HEIGHT = `${FIXED_CELL_HEIGHT_NUMERIC}px`;

interface CalendarDayProps {
  dayData: CalendarDayData;
  singleDayEvents?: CalendarEvent[];
  multiDaySpacerHeight: number;
  onShowMoreClick: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
}

export const CalendarDay: React.FC<CalendarDayProps> = ({
  dayData,
  singleDayEvents = [],
  multiDaySpacerHeight,
  onShowMoreClick,
}) => {
  const { date, isCurrentMonth, isWeekend } = dayData;
  const isToday = isTodayDateFns(date);
  const dayNumber = format(date, 'd');

  const getDayStyles = (): React.CSSProperties => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    justifyContent: 'flex-start',
    padding: '4px',
    height: FIXED_CELL_HEIGHT,
    borderRight: '1px solid #eee',
    borderBottom: '1px solid #eee',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease',
    backgroundColor: '#fff',
    opacity: isCurrentMonth ? 1 : 0.4,
    position: 'relative',
    overflow: 'hidden',
    color: !isCurrentMonth ? '#9e9e9e' : 'inherit',
  });

  const getNumberStyles = (): React.CSSProperties => {
    const styles: React.CSSProperties = {
      width: '24px',
      height: '24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: '50%',
      fontSize: '0.8rem',
      fontWeight: isToday ? 'bold' : 'normal',
      color: !isCurrentMonth ? '#9e9e9e' : isWeekend ? '#f44336' : 'inherit',
    };
    if (isToday) {
      styles.backgroundColor = '#1976d2';
      styles.color = '#fff';
    }
    return styles;
  };

  const availableSpaceForSingleEvents =
    FIXED_CELL_HEIGHT_NUMERIC - DATE_NUMBER_AREA_HEIGHT - multiDaySpacerHeight - 8;

  const { visibleEvents, hiddenCount, showMoreLink } = calculateVisibleLayout({
    allSingleEvents: singleDayEvents,
    maxOverallVisible: MAX_VISIBLE_SINGLE_DAY_EVENTS,
    availableHeight: availableSpaceForSingleEvents,
  });

  return (
    <Box sx={getDayStyles()}>
      <Box
        sx={{
          alignSelf: 'flex-end',
          mb: 0.5,
          mr: 0.5,
          height: `${DATE_NUMBER_AREA_HEIGHT}px`,
          boxSizing: 'border-box',
          flexShrink: 0,
        }}
      >
        <Typography variant="body2" sx={getNumberStyles()}>
          {dayNumber}
        </Typography>
      </Box>

      <Box sx={{ height: `${multiDaySpacerHeight}px`, flexShrink: 0 }} />

      <Stack spacing={0.2} sx={{ width: '100%', pl: '2px', flexGrow: 1, overflow: 'hidden' }}>
        {visibleEvents.map((event) => (
          <EventItem key={event.id} event={event} />
        ))}

        {showMoreLink && hiddenCount > 0 && (
          <Typography
            variant="caption"
            onClick={(e) => onShowMoreClick(e, date)}
            sx={{
              pl: '2px',
              fontSize: '0.65rem',
              color: 'text.secondary',
              cursor: 'pointer',
              mt: '2px',
              '&:hover': {
                textDecoration: 'underline',
              },
            }}
          >
            +{hiddenCount} more
          </Typography>
        )}
      </Stack>
    </Box>
  );
};
