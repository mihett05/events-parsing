import { CalendarEvent } from '@entities/Event';
import { ESTIMATED_SINGLE_EVENT_HEIGHT, ESTIMATED_MORE_LINK_HEIGHT } from '@widgets/MonthCalendar/lib/constants';

interface CalculateVisibleLayoutParams {
  allSingleEvents: CalendarEvent[];
  maxOverallVisible: number;
  availableHeight: number;
}

interface CalculatedLayout {
  visibleEvents: CalendarEvent[];
  hiddenCount: number;
  showMoreLink: boolean;
}

export const calculateVisibleLayout = ({
  allSingleEvents,
  maxOverallVisible,
  availableHeight,
}: CalculateVisibleLayoutParams): CalculatedLayout => {
  const totalEvents = allSingleEvents.length;
  let maxFit = 0;

  if (availableHeight > 0 && ESTIMATED_SINGLE_EVENT_HEIGHT > 0) {
    maxFit = Math.floor(availableHeight / ESTIMATED_SINGLE_EVENT_HEIGHT);
  }

  const numToShow = Math.min(totalEvents, maxOverallVisible, maxFit);
  const hiddenEventsCount = totalEvents - numToShow;
  let showMoreLink = false;
  let finalNumToShow = numToShow;

  if (hiddenEventsCount > 0) {
    const spaceNeededWithLink =
      numToShow * ESTIMATED_SINGLE_EVENT_HEIGHT + ESTIMATED_MORE_LINK_HEIGHT;

    if (spaceNeededWithLink <= availableHeight) {
      showMoreLink = true;
    } else {
      const numToShowMinusOne = Math.max(0, numToShow - 1);
      const spaceNeededWithLinkAndLessItem =
        numToShowMinusOne * ESTIMATED_SINGLE_EVENT_HEIGHT + ESTIMATED_MORE_LINK_HEIGHT;

      if (numToShow > 0 && spaceNeededWithLinkAndLessItem <= availableHeight) {
        showMoreLink = true;
        finalNumToShow = numToShowMinusOne;
      } else {
        showMoreLink = false;
        finalNumToShow = numToShow;
      }
    }
  }

  const finalHiddenCount = totalEvents - finalNumToShow;
  const visibleEvents = allSingleEvents.slice(0, finalNumToShow);

  if (finalHiddenCount <= 0) {
    showMoreLink = false;
  }

  return {
    visibleEvents,
    hiddenCount: finalHiddenCount,
    showMoreLink,
  };
};
