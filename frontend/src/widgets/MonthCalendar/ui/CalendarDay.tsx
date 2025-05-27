import React, { useMemo } from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { format, isToday as isTodayDateFns, isValid } from 'date-fns';
import { ru } from 'date-fns/locale';
import { CalendarDayData } from '@shared/lib/types';
import { CalendarEvent, EventItem } from '@entities/Event';
import { isEventOnDate } from '@widgets/MonthCalendar/lib/eventUtils';
import { DATE_NUMBER_AREA_HEIGHT } from '@widgets/MonthCalendar/lib/constants';
import { SxProps, Theme } from '@mui/material';
import { useTranslation } from 'react-i18next';

const MAX_VISIBLE_EVENTS_IN_CELL = 2;
const FIXED_CELL_HEIGHT_NUMERIC = 120;
const FIXED_CELL_HEIGHT = `${FIXED_CELL_HEIGHT_NUMERIC}px`;

interface CalendarDayProps {
  dayData: CalendarDayData;
  events: CalendarEvent[];
  onDayClick: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
}

export const CalendarDay: React.FC<CalendarDayProps> = ({ dayData, events, onDayClick }) => {
  const { t } = useTranslation();
  if (!dayData?.date || !isValid(dayData.date)) {
    console.error('CalendarDay received invalid dayData:', dayData);
    return (
      <Box
        sx={(theme: Theme) => ({
          height: FIXED_CELL_HEIGHT,
          borderRight: `1px solid ${theme.palette.divider}`,
          borderBottom: `1px solid ${theme.palette.divider}`,
          p: 1,
          fontSize: '0.8rem',
          color: 'error.main',
          overflow: 'hidden',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: theme.palette.mode === 'light' ? '#fff3f3' : '#5c2a2a',
        })}
      >
        {t('calendar.invalidDate')}
      </Box>
    );
  }
  const { date, isCurrentMonth, isWeekend } = dayData;
  const isToday = isTodayDateFns(date);
  const dayNumber = format(date, 'd');
  const formattedFullDate = format(date, 'PPP', { locale: ru });

  const eventsForThisDay = useMemo(() => {
    return events
      .filter((event) => event && isEventOnDate(event, date))
      .sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
  }, [events, date]);

  const visibleEvents = eventsForThisDay.slice(0, MAX_VISIBLE_EVENTS_IN_CELL);
  const hiddenCount = Math.max(0, eventsForThisDay.length - MAX_VISIBLE_EVENTS_IN_CELL);
  const hasEvents = eventsForThisDay.length > 0;

  const getDayStyles = (): SxProps<Theme> => ({
    display: 'flex',
    flexDirection: 'column',
    height: FIXED_CELL_HEIGHT,
    borderRight: '1px solid #eee',
    borderBottom: '1px solid #eee',
    cursor: 'pointer',
    transition: 'background-color 0.15s ease',
    backgroundColor: isCurrentMonth ? 'background.paper' : '#fafafa',
    position: 'relative',
    overflow: 'hidden',
    color: isCurrentMonth ? 'text.primary' : 'text.disabled',
    '&:hover': {
      backgroundColor: isCurrentMonth ? 'action.hover' : '#f0f0f0',
      zIndex: 1,
    },
    '&:nth-of-type(7n)': {
      borderRight: 'none',
    },
  });
  const getNumberStyles = (): SxProps<Theme> => ({
    width: '24px',
    height: '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '50%',
    fontSize: '0.75rem',
    lineHeight: 1,
    fontWeight: isToday ? 'bold' : 'normal',
    color: isToday
      ? 'primary.contrastText'
      : !isCurrentMonth
        ? 'text.disabled'
        : isWeekend
          ? 'error.main'
          : 'text.primary',
    backgroundColor: isToday ? 'primary.main' : 'transparent',
    marginLeft: 'auto',
    flexShrink: 0,
  });

  const handleCellClick = (e: React.MouseEvent<HTMLElement>) => {
    onDayClick(e, date);
  };

  return (
    <Box
      sx={getDayStyles()}
      onClick={handleCellClick}
      title={
        hasEvents ? t('calendar.popoverTitle', { date: formattedFullDate }) : formattedFullDate
      }
      role={hasEvents ? 'button' : 'gridcell'}
      aria-label={
        hasEvents ? t('calendar.popoverTitle', { date: formattedFullDate }) : formattedFullDate
      }
      tabIndex={hasEvents ? 0 : -1}
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
        <Typography variant="body2" component="span" sx={getNumberStyles()}>
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
              pl: '4px',
              pointerEvents: 'none',
              userSelect: 'none',
            }}
          >
            {t('calendar.moreEvents', { count: hiddenCount })}
          </Typography>
        )}
      </Stack>
    </Box>
  );
};
