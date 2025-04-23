import { useReadAllEventsV1EventsGetQuery } from '@/shared/api/api';
import { useAppDispatch, useAppSelector } from '@shared/store/hooks';
import { incrementPage, eventsAdapter } from '@features/events/slice';

export const useEventsFeed = () => {
  const dispatch = useAppDispatch();
  const state = useAppSelector((state) => state.events);
  const events = eventsAdapter.getSelectors().selectAll(state.events);

  useReadAllEventsV1EventsGetQuery({
    page: state.page,
    pageSize: state.pageSize,
  });

  const handleLoadMore = () => {
    dispatch(incrementPage());
  };

  return {
    events,
    isLoading: state.isLoading,
    error: state.error,
    handleLoadMore,
  };
};
