import { useCallback } from 'react';
import { useReadAllEventsV1EventsFeedGetQuery } from '@/shared/api/api';
import { useAppDispatch, useAppSelector } from '@shared/store/hooks';
import {
  incrementPage,
  selectEventsError,
  selectEventsCurrentPage,
  selectEventsLoading,
  selectEventsFetchingMore,
  selectFilteredCalendarEvents,
} from '@features/events/slice';
import { RootState } from '@/shared/store/store';

export const useEventsFeed = () => {
  const dispatch = useAppDispatch();

  const page = useAppSelector(selectEventsCurrentPage);
  const pageSize = useAppSelector((state: RootState) => state.events.pageSize);
  const events = useAppSelector(selectFilteredCalendarEvents);
  const errorKey = useAppSelector(selectEventsError);
  const isLoading = useAppSelector(selectEventsLoading);
  const isFetchingMore = useAppSelector(selectEventsFetchingMore);

  const queryArgs = {
    page,
    pageSize,
  };

  const { isFetching, error: queryError } = useReadAllEventsV1EventsFeedGetQuery(queryArgs);

  const handleLoadMore = useCallback(() => {
    if (!isLoading && !isFetchingMore && !isFetching) {
      dispatch(incrementPage());
    }
  }, [dispatch, isLoading, isFetchingMore, isFetching]);

  const errorMessage = errorKey
    ? { messageKey: errorKey, messageOptions: { message: queryError ? String(queryError) : '' } }
    : null;

  return {
    events,
    isLoading: isLoading || (isFetching && page === 0),
    isFetchingMore: isFetchingMore || (isFetching && page > 0),
    error: errorMessage,
    handleLoadMore,
    currentPage: page,
  };
};
