import React, { useMemo } from 'react';
import { Box, Typography, Tooltip } from '@mui/material';
import {
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  format,
  getDay as getDayOfWeek,
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
import { isEventOnDate } from '@/widgets/MonthCalendar/lib/eventUtils';
import { Theme } from '@mui/material/styles';
import { SystemStyleObject } from '@mui/system';

interface MiniMonthProps {
  monthDate: Date;
  events: CalendarEvent[];
  year: number;
  onMonthClick: (date: Date) => void;
  onDayClick: (date: Date) => void;
}

const WEEK_STARTS_ON = 1;

const getDayStyle = (
  day: Date,
  isCurrentMonth: boolean,
  daysWithEventsSet: Set<string>,
  theme: Theme,
): SystemStyleObject<Theme> => {
  const isCurrentDateToday = isToday(day);
  const dayOfWeek = getDayOfWeek(day);
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
    backgroundColor = theme.palette.action.hover;
  } else if (isCurrentMonth && isWeekend) {
    textColor = theme.palette.error.main;
  } else if (!isCurrentMonth) {
    textColor = theme.palette.text.disabled;
  }

  return {
    width: { xs: 24, sm: 28 },
    height: { xs: 24, sm: 28 },
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '50%',
    fontSize: { xs: '0.7rem', sm: '0.75rem' },
    fontWeight: fontWeight,
    color: textColor,
    backgroundColor: backgroundColor,
    transition: 'background-color 0.2s ease-out, color 0.2s ease-out',
    position: 'relative',
    ...(isCurrentMonth && {
      cursor: 'pointer',
      '&:hover': {
        bgcolor: isCurrentDateToday ? theme.palette.primary.dark : theme.palette.action.selected,
      },
    }),
    ...(!isCurrentMonth && {
      cursor: 'default',
    }),
  };
};

export const MiniMonth: React.FC<MiniMonthProps> = React.memo(
  ({ monthDate, events, year, onMonthClick, onDayClick }) => {
    const { t } = useTranslation();

    const monthIndex = useMemo(() => getMonth(monthDate), [monthDate]);

    const monthName = useMemo(() => {
      if (!isValid(monthDate)) return '';
      const name = format(monthDate, 'LLLL', { locale: ru });
      return name.charAt(0).toUpperCase() + name.slice(1);
    }, [monthDate]);

    const daysInMonthGrid = useMemo(() => {
      if (!isValid(monthDate)) return [];
      const monthStart = startOfMonth(monthDate);
      const startDateGrid = startOfWeek(monthStart, {
        weekStartsOn: WEEK_STARTS_ON,
      });
      const endDateGrid = addDays(startDateGrid, 6 * 7 - 1);
      return eachDayOfInterval({ start: startDateGrid, end: endDateGrid });
    }, [monthDate]);

    const daysWithEventsSet = useMemo(() => {
      if (!isValid(monthDate)) return new Set<string>();
      const currentMonthStart = startOfMonth(monthDate);
      const currentMonthEnd = endOfMonth(monthDate);
      const daysSet = new Set<string>();

      const relevantEvents = events.filter((event) => {
        if (!event || !isValid(event.startDate)) return false;
        const eventStart = event.startDate;
        const eventEnd = event.endDate && isValid(event.endDate) ? event.endDate : eventStart;
        return eventStart <= currentMonthEnd && eventEnd >= currentMonthStart;
      });

      const daysInCurrentDisplayMonth = eachDayOfInterval({
        start: currentMonthStart,
        end: currentMonthEnd,
      });
      daysInCurrentDisplayMonth.forEach((dayOfMonth) => {
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

    const handleInternalMonthClick = () => {
      if (!isValid(monthDate)) return;
      onMonthClick(startOfMonth(monthDate));
    };

    const handleInternalDayClick = (day: Date, isCurrentMonth: boolean, e: React.MouseEvent) => {
      e.stopPropagation();
      if (!isValid(day) || !isCurrentMonth) return;
      onDayClick(day);
    };

    return (
      <Box sx={{ p: 1, height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Typography
          variant="subtitle2"
          align="center"
          gutterBottom
          onClick={handleInternalMonthClick}
          title={t('calendar.view.month') + ' ' + format(monthDate, 'LLLL yyyy', { locale: ru })}
          sx={{
            fontWeight: 500,
            cursor: 'pointer',
            '&:hover': { color: 'primary.main' },
            mb: 1,
            userSelect: 'none',
          }}
        >
          {monthName}
        </Typography>
        <Box
          sx={{
            flexGrow: 1,
            display: 'grid',
            gridTemplateColumns: 'repeat(7, 1fr)',
            gap: { xs: '2px', sm: '3px', md: 0.5 },
            alignItems: 'center',
            justifyItems: 'center',
          }}
        >
          {daysInMonthGrid.map((day, index) => {
            if (!isValid(day)) {
              return (
                <Box
                  key={`invalid-day-${index}`}
                  sx={{ minHeight: { xs: 24, sm: 28 }, width: '100%' }}
                />
              );
            }
            const isCurrentMonthView = getMonth(day) === monthIndex && getYear(day) === year;
            const formattedDayNumber = format(day, 'd');
            const dateStringKey = format(day, 'yyyy-MM-dd-HH-mm-ss-ms');
            return (
              <Tooltip
                key={dateStringKey}
                title={isCurrentMonthView ? format(day, 'PPP', { locale: ru }) : ''}
                arrow
                placement="top"
                disableHoverListener={!isCurrentMonthView}
                enterDelay={500}
                enterNextDelay={500}
              >
                <Box
                  sx={(theme: Theme) =>
                    getDayStyle(day, isCurrentMonthView, daysWithEventsSet, theme)
                  }
                  onClick={(e: React.MouseEvent) =>
                    handleInternalDayClick(day, isCurrentMonthView, e)
                  }
                >
                  {formattedDayNumber}
                </Box>
              </Tooltip>
            );
          })}
        </Box>
      </Box>
    );
  },
);
