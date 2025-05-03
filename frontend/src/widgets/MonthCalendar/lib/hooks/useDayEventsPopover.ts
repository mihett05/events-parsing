import { useState, useCallback } from 'react';
import { isValid } from 'date-fns';

interface UseDayEventsPopoverReturn {
  popoverId: string | undefined;
  isPopoverOpen: boolean;
  popoverAnchorEl: HTMLElement | null;
  selectedDateForPopover: Date | null;
  openPopover: (event: React.MouseEvent<HTMLElement>, date: Date) => void;
  closePopover: () => void;
}

export const useDayEventsPopover = (): UseDayEventsPopoverReturn => {
  const [popoverAnchorEl, setPopoverAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedDateForPopover, setSelectedDateForPopover] = useState<null | Date>(null);

  const openPopover = useCallback((event: React.MouseEvent<HTMLElement>, date: Date) => {
    if (isValid(date)) {
      setSelectedDateForPopover(date);
      setPopoverAnchorEl(event.currentTarget);
    } else {
      setPopoverAnchorEl(null);
      setSelectedDateForPopover(null);
    }
  }, []);

  const closePopover = useCallback(() => {
    setPopoverAnchorEl(null);
  }, []);

  const isPopoverOpen = !!popoverAnchorEl;
  const popoverId = isPopoverOpen ? 'day-events-popover' : undefined;

  return {
    popoverId,
    isPopoverOpen,
    popoverAnchorEl,
    selectedDateForPopover,
    openPopover,
    closePopover,
  };
};
