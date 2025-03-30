import React, { useMemo, useRef } from 'react';
import { Box, Paper, Popover } from '@mui/material';
import { CalendarEvent } from '../../../entities/Event';
import {
  getDayNames,
  useGridDimensions,
  useDayEventsPopover,
  useCalendarNavigation,
  useCalendarData,
} from '../lib';
import { CalendarHeader } from './components/CalendarHeader';
import { DayNamesHeader } from './components/DayNamesHeader';
import { CalendarGrid } from './components/CalendarGrid';
import { MultiDayEventOverlay } from './components/MultiDayEventOverlay';
import { DayEventsPopoverContent } from './components/DayEventsPopoverContent';

interface MonthCalendarProps {
  events?: CalendarEvent[];
  initialDate?: Date;
}

export const MonthCalendar: React.FC<MonthCalendarProps> = ({ events = [], initialDate }) => {
  const gridContainerRef = useRef<HTMLDivElement>(null);

  const { currentDate, handlePrevMonth, handleNextMonth, handleToday } = useCalendarNavigation({
    initialDate,
  });

  const {
    calendarDays,
    singleDayEventsByDate,
    multiDayEvents,
    multiDayLayout,
    spacerHeightsPerWeek,
  } = useCalendarData({ currentDate, events });

  const dayNames = useMemo(() => getDayNames(0), []);

  const {
    popoverId,
    isPopoverOpen,
    popoverAnchorEl,
    popoverContentProps,
    handleShowMoreClick,
    handlePopoverClose,
  } = useDayEventsPopover({ singleDayEventsByDate, multiDayEvents });

  const { cellWidth, rowHeight, headerHeight } = useGridDimensions(gridContainerRef, [
    calendarDays,
  ]);

  return (
    <Paper
      elevation={0}
      sx={{
        p: 1,
        maxWidth: '100%',
        border: '1px solid #eee',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <CalendarHeader
        currentDate={currentDate}
        onPrevMonth={handlePrevMonth}
        onNextMonth={handleNextMonth}
        onToday={handleToday}
      />

      <Box
        ref={gridContainerRef}
        sx={{
          position: 'relative',
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        <DayNamesHeader dayNames={dayNames} height={`${headerHeight}px`} />
        <CalendarGrid
          ref={gridContainerRef}
          calendarDays={calendarDays}
          singleDayEventsByDate={singleDayEventsByDate}
          spacerHeightsPerWeek={spacerHeightsPerWeek}
          onShowMoreClick={handleShowMoreClick}
        />
        <MultiDayEventOverlay
          multiDayLayout={multiDayLayout}
          cellWidth={cellWidth}
          rowHeight={rowHeight}
          headerHeight={headerHeight}
        />
      </Box>
      <Popover
        id={popoverId}
        open={isPopoverOpen}
        anchorEl={popoverAnchorEl}
        onClose={handlePopoverClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'left' }}
        slotProps={{ paper: { sx: {} } }}
      >
        {popoverContentProps.date && (
          <DayEventsPopoverContent
            date={popoverContentProps.date}
            singleEvents={popoverContentProps.singleEvents}
            multiDayEvents={popoverContentProps.multiEvents}
            onClose={handlePopoverClose}
          />
        )}
      </Popover>
    </Paper>
  );
};
