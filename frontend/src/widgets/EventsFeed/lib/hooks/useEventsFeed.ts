import { useCallback, useEffect, useRef, useMemo, useState } from 'react';
import {
  useReadAllEventsV1EventsFeedGetQuery,
  ReadAllEventsV1EventsFeedGetApiArg,
} from '@/shared/api/api';
import { useAppDispatch, useAppSelector } from '@shared/store/hooks';
import {
  incrementPage,
  setPage,
  selectEventsCurrentPage,
  FilterState,
  selectAllEvents,
} from '@features/events/slice';
import { RootState } from '@/shared/store/store';

export const useEventsFeed = (currentFilters: FilterState) => {
  const dispatch = useAppDispatch();
  const page = useAppSelector(selectEventsCurrentPage);
  const pageSize = useAppSelector((state: RootState) => state.events.pageSize);

  const { type, format, organizationId } = currentFilters;

  const [hasMore, setHasMore] = useState(true);

  const queryArgs = useMemo((): ReadAllEventsV1EventsFeedGetApiArg => {
    const args: ReadAllEventsV1EventsFeedGetApiArg = { page, pageSize };
    if (organizationId !== null) args.organizationId = organizationId;
    if (type !== null) args.type = type;
    if (format !== null) args.format = format;
    return args;
  }, [page, pageSize, type, format, organizationId]);

  const {
    data: currentFetchData,
    isFetching,
    isLoading: rtkQueryIsLoading,
    error: currentQueryError,
    isError: isCurrentQueryError,
    isSuccess: isCurrentQuerySuccess,
  } = useReadAllEventsV1EventsFeedGetQuery(queryArgs, {
    refetchOnMountOrArgChange: true,
  });

  const isInitialMount = useRef(true);

  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    dispatch(setPage(0));
    setHasMore(true);
  }, [type, format, organizationId, dispatch]);

  useEffect(() => {
    if (isCurrentQuerySuccess && currentFetchData) {
      setHasMore(currentFetchData.length === pageSize);
    } else if (isCurrentQueryError) {
      setHasMore(false);
    }
  }, [currentFetchData, isCurrentQuerySuccess, isCurrentQueryError, pageSize]);

  const eventsFromStore = useAppSelector(selectAllEvents);

  const handleLoadMore = useCallback(() => {
    if (!isFetching && hasMore) {
      dispatch(incrementPage());
    }
  }, [dispatch, isFetching, hasMore]);

  let displayError: { messageKey: string } | null = null;
  if (isCurrentQueryError && currentQueryError && !isFetching) {
    const apiError = currentQueryError as any;
    displayError = {
      messageKey:
        apiError?.data?.detail?.[0]?.msg || apiError?.data?.message || 'feed.errorLoading',
    };
  }

  const isLoadingState = (rtkQueryIsLoading || isFetching) && page === 0;
  const isFetchingMoreState = isFetching && page > 0;

  return {
    events: eventsFromStore,
    isLoading: isLoadingState,
    isFetchingMore: isFetchingMoreState,
    error: displayError,
    handleLoadMore,
    currentPage: page,
    hasMore,
  };
};
