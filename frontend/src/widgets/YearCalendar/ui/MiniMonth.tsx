import React, { useMemo } from 'react';
import { Box, Typography, Grid, Tooltip } from '@mui/material';
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
    fontWeight = 'bold';
  } else if (isCurrentMonth && (getDay(day) === 0 || getDay(day) === 6)) {
    textColor = theme.palette.error.main;
  }

  if (!isCurrentMonth) {
    textColor = theme.palette.text.disabled;
    backgroundColor = 'transparent';
    fontWeight = 'normal';
  }

  return {
    width: 24,
    height: 24,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '50%',
    fontSize: '0.65rem',
    cursor: 'pointer',
    fontWeight: fontWeight,
    color: textColor,
    backgroundColor: backgroundColor,
    transition: 'background-color 0.2s ease-out, color 0.2s ease-out',
    position: 'relative',
    '&:hover': {
      bgcolor:
        isCurrentDateToday && isCurrentMonth
          ? theme.palette.primary.dark
          : theme.palette.action.hover,
    },
  };
};

export const MiniMonth: React.FC<MiniMonthProps> = React.memo(({ monthDate, events, year }) => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();

  const monthIndex = getMonth(monthDate);
  const monthName = t(
    `calendar.monthNames.${monthIndex}`,
    format(monthDate, 'LLLL', { locale: ru }),
  );

  const daysInMonthGrid = useMemo(() => {
    const monthStart = startOfMonth(monthDate);
    const startDate = startOfWeek(monthStart, { weekStartsOn: WEEK_STARTS_ON });
    const endDate = addDays(startDate, 41);
    return eachDayOfInterval({ start: startDate, end: endDate });
  }, [monthDate]);

  const daysWithEventsSet = useMemo(() => {
    const monthStart = startOfMonth(monthDate);
    const monthEnd = endOfMonth(monthDate);
    const daysSet = new Set<string>();
    const relevantEvents = events.filter((event) => {
      if (!event || !isValid(event.startDate)) return false;
      const eventStart = event.startDate;
      const eventEnd = event.endDate && isValid(event.endDate) ? event.endDate : eventStart;
      return eventStart <= monthEnd && eventEnd >= monthStart;
    });
    const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
    daysInMonth.forEach((dayOfMonth) => {
      for (const event of relevantEvents) {
        if (isEventOnDate(event, dayOfMonth)) {
          daysSet.add(format(dayOfMonth, 'yyyy-MM-dd'));
          break;
        }
      }
    });
    return daysSet;
  }, [events, monthDate]);

  const handleMonthClick = () => {
    dispatch(setSelectedDate(startOfMonth(monthDate).toISOString()));
    dispatch(setCalendarView('month'));
  };

  const handleDayClick = (day: Date, e: React.MouseEvent) => {
    e.stopPropagation();
    dispatch(setSelectedDate(day.toISOString()));
    dispatch(setCalendarView('day'));
  };

  return (
    <Box sx={{ p: 1 }}>
      <Typography
        variant="subtitle2"
        align="center"
        gutterBottom
        sx={{ fontWeight: 500, cursor: 'pointer', '&:hover': { color: 'primary.main' } }}
        onClick={handleMonthClick}
        title={t('calendar.view.month') + ' ' + monthName.toLowerCase()}
      >
        {monthName}
      </Typography>
      <Grid container columns={7} spacing={0.5} sx={{ minHeight: 150 }}>
        {daysInMonthGrid.map((day) => {
          const isCurrentMonth = getMonth(day) === monthIndex && getYear(day) === year;
          const formattedDayNumber = format(day, 'd');
          const dateStringKey = format(day, 'yyyy-MM-dd');
          const hasEvent = isCurrentMonth && daysWithEventsSet.has(dateStringKey);
          return (
            <Grid
              key={dateStringKey}
              sx={{ display: 'flex', justifyContent: 'center', width: `${100 / 7}%` }}
            >
              <Tooltip
                title={
                  hasEvent ? format(day, 'PPP', { locale: ru }) : t('yearView.noEventsIndicator')
                }
                arrow
                placement="top"
                disableHoverListener={!isCurrentMonth}
              >
                <Box
                  sx={(theme: Theme): SystemStyleObject<Theme> =>
                    getDayStyle(day, isCurrentMonth, daysWithEventsSet, theme)
                  }
                  onClick={(e: React.MouseEvent) => handleDayClick(day, e)}
                >
                  {isCurrentMonth ? formattedDayNumber : ''}
                </Box>
              </Tooltip>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
});
