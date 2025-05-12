import React, { useMemo } from 'react';
import { Box, Typography, Tooltip } from '@mui/material';
import {
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  format,
  getDay,
  isToday,
  startOfWeek,
  addDays,
  isValid,
  getMonth,
  getYear,
} from 'date-fns';
import { ru } from 'date-fns/locale';
import { CalendarEvent } from '@/entities/Event';
import { useTranslation } from 'react-i18next';
import { useAppDispatch } from '@/shared/store/hooks';
import { setCalendarView, setSelectedDate } from '@/features/events/slice';
import { isEventOnDate } from '@/widgets/MonthCalendar/lib/eventUtils';
import { Theme } from '@mui/material/styles';
import { SystemStyleObject } from '@mui/system';

interface MiniMonthProps {
  monthDate: Date;
  events: CalendarEvent[];
  year: number;
}

const WEEK_STARTS_ON = 1;

const getDayStyle = (
  day: Date,
  isCurrentMonth: boolean,
  daysWithEventsSet: Set<string>,
  theme: Theme,
): SystemStyleObject<Theme> => {
  const isCurrentDateToday = isToday(day);
  const dayOfWeek = getDay(day);
  const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
  const hasEvent = isCurrentMonth && daysWithEventsSet.has(format(day, 'yyyy-MM-dd'));

  let backgroundColor = 'transparent';
  let fontWeight = 'normal';
  let textColor = theme.palette.text.primary;

  if (isCurrentDateToday && isCurrentMonth) {
    backgroundColor = theme.palette.primary.main;
    textColor = theme.palette.primary.contrastText;
    fontWeight = 'bold';
  } else if (hasEvent) {
    backgroundColor = theme.palette.action.selected;
  } else if (isCurrentMonth && isWeekend) {
    textColor = theme.palette.error.main;
  } else if (!isCurrentMonth) {
    textColor = theme.palette.text.disabled;
  }

  return {
    width: 28,
    height: 28,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '50%',
    fontSize: '0.75rem',
    fontWeight: fontWeight,
    color: textColor,
    backgroundColor: backgroundColor,
    transition: 'background-color 0.2s ease-out, color 0.2s ease-out',
    position: 'relative',
    ...(isCurrentMonth && {
      cursor: 'pointer',
      '&:hover': {
        bgcolor: isCurrentDateToday ? theme.palette.primary.dark : theme.palette.action.hover,
      },
    }),
    ...(!isCurrentMonth && {
      cursor: 'default',
    }),
  };
};

export const MiniMonth: React.FC<MiniMonthProps> = React.memo(({ monthDate, events, year }) => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();

  const monthIndex = useMemo(() => getMonth(monthDate), [monthDate]);

  const monthName = useMemo(() => {
    if (!isValid(monthDate)) return '';
    const name = format(monthDate, 'LLLL', { locale: ru });
    return name.charAt(0).toUpperCase() + name.slice(1);
  }, [monthDate]);

  const daysInMonthGrid = useMemo(() => {
    if (!isValid(monthDate)) return [];
    const monthStart = startOfMonth(monthDate);
    const startDate = startOfWeek(monthStart, {
      weekStartsOn: WEEK_STARTS_ON,
      locale: ru,
    });
    const endDate = addDays(startDate, 41);
    return eachDayOfInterval({ start: startDate, end: endDate });
  }, [monthDate]);

  const daysWithEventsSet = useMemo(() => {
    if (!isValid(monthDate)) return new Set<string>();
    const monthStart = startOfMonth(monthDate);
    const monthEnd = endOfMonth(monthDate);
    const daysSet = new Set<string>();
    const relevantEvents = events.filter((event) => {
      if (!event || !isValid(event.startDate)) return false;
      const eventStart = event.startDate;
      const eventEnd = event.endDate && isValid(event.endDate) ? event.endDate : eventStart;
      return eventStart <= monthEnd && eventEnd >= monthStart;
    });
    const daysInCurrentMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
    daysInCurrentMonth.forEach((dayOfMonth) => {
      const dayFormatted = format(dayOfMonth, 'yyyy-MM-dd');
      for (const event of relevantEvents) {
        if (isEventOnDate(event, dayOfMonth)) {
          daysSet.add(dayFormatted);
          break;
        }
      }
    });
    return daysSet;
  }, [events, monthDate]);

  const handleMonthClick = () => {
    if (!isValid(monthDate)) return;
    dispatch(setSelectedDate(startOfMonth(monthDate).toISOString()));
    dispatch(setCalendarView('month'));
  };

  const handleDayClick = (day: Date, isCurrentMonth: boolean, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isValid(day) || !isCurrentMonth) return;
    dispatch(setSelectedDate(day.toISOString()));
    dispatch(setCalendarView('day'));
  };

  return (
    <Box sx={{ p: 1, height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography
        variant="subtitle2"
        align="center"
        gutterBottom
        onClick={handleMonthClick}
        title={t('calendar.view.month') + ' ' + format(monthDate, 'LLLL yyyy', { locale: ru })}
        sx={{
          fontWeight: 500,
          cursor: 'pointer',
          '&:hover': { color: 'primary.main' },
          mb: 1,
        }}
      >
        {monthName}
      </Typography>
      <Box
        sx={{
          flexGrow: 1,
          display: 'grid',
          gridTemplateColumns: 'repeat(7, 1fr)',
          gap: { xs: 0.2, sm: 0.5 },
          alignItems: 'center',
          justifyItems: 'center',
        }}
      >
        {daysInMonthGrid.map((day) => {
          if (!isValid(day)) {
            return <Box key={Math.random()} sx={{ minHeight: 32, width: '100%' }} />;
          }
          const isCurrentMonth = getMonth(day) === monthIndex && getYear(day) === year;
          const formattedDayNumber = format(day, 'd');
          const dateStringKey = format(day, 'yyyy-MM-dd');

          return (
            <Tooltip
              key={dateStringKey}
              title={isCurrentMonth ? format(day, 'PPP', { locale: ru }) : ''}
              arrow
              placement="top"
              disableHoverListener={!isCurrentMonth}
              enterDelay={500}
              enterNextDelay={500}
            >
              <Box
                sx={(theme: Theme) => getDayStyle(day, isCurrentMonth, daysWithEventsSet, theme)}
                onClick={(e: React.MouseEvent) => handleDayClick(day, isCurrentMonth, e)}
              >
                {formattedDayNumber}
              </Box>
            </Tooltip>
          );
        })}
      </Box>
    </Box>
  );
});
