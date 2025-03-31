import React, { useState, useCallback } from 'react';
import { format, isWithinInterval, startOfDay, endOfDay } from 'date-fns';
import { CalendarEvent } from '@entities/Event';

interface UseDayEventsPopoverProps {
  singleDayEventsByDate: Record<string, CalendarEvent[]>;
  multiDayEvents: CalendarEvent[];
}

interface PopoverState {
  anchorEl: HTMLElement | null;
  date: Date | null;
  singleEvents: CalendarEvent[];
  multiEvents: CalendarEvent[];
}

export const useDayEventsPopover = ({
  singleDayEventsByDate,
  multiDayEvents,
}: UseDayEventsPopoverProps) => {
  const [popoverState, setPopoverState] = useState<PopoverState>({
    anchorEl: null,
    date: null,
    singleEvents: [],
    multiEvents: [],
  });

  const handleShowMoreClick = useCallback(
    (event: React.MouseEvent<HTMLElement>, date: Date) => {
      const dateKey = format(date, 'yyyy-MM-dd');
      const singleForDay = singleDayEventsByDate[dateKey] || [];

      const multiForDay = multiDayEvents.filter((ev) => {
        if (!ev.endDate) return false;
        const dayStart = startOfDay(date);
        const dayEnd = endOfDay(date);
        const eventStart = startOfDay(ev.startDate);
        const eventEnd = endOfDay(ev.endDate);

        return (
          isWithinInterval(dayStart, { start: eventStart, end: eventEnd }) ||
          isWithinInterval(dayEnd, { start: eventStart, end: eventEnd }) ||
          (eventStart < dayStart && eventEnd > dayEnd)
        );
      });

      setPopoverState({
        anchorEl: event.currentTarget,
        date: date,
        singleEvents: singleForDay,
        multiEvents: multiForDay,
      });
    },
    [singleDayEventsByDate, multiDayEvents],
  );

  const handlePopoverClose = useCallback(() => {
    setPopoverState({
      anchorEl: null,
      date: null,
      singleEvents: [],
      multiEvents: [],
    });
  }, []);

  const open = Boolean(popoverState.anchorEl);
  const id = open ? 'day-events-popover' : undefined;

  return {
    popoverId: id,
    isPopoverOpen: open,
    popoverAnchorEl: popoverState.anchorEl,
    popoverContentProps: {
      date: popoverState.date,
      singleEvents: popoverState.singleEvents,
      multiEvents: popoverState.multiEvents,
    },
    handleShowMoreClick,
    handlePopoverClose,
  };
};
