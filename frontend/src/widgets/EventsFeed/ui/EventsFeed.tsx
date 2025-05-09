import React, { useEffect, useRef } from 'react';
import { EventArticle } from '@/entities/Event';
import { Box, Divider, CircularProgress } from '@mui/material';
import { useEventsFeed } from '../lib/hooks';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { CalendarFilters } from '@/features/events/filter/ui/EventsFilter';

export const EventsFeed = () => {
  const { events, isLoading, isFetchingMore, error, handleLoadMore } = useEventsFeed();

  const observer = useRef<IntersectionObserver | null>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (observer.current) {
      observer.current.disconnect();
    }

    observer.current = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          handleLoadMore();
        }
      });
    });

    if (sentinelRef.current) {
      observer.current.observe(sentinelRef.current);
    }

    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, [handleLoadMore]);

  if (isLoading && events.length === 0) {
    return <LoadingIndicator />;
  }

  if (error && events.length === 0) {
    return <ErrorMessage {...error} />;
  }

  return (
    <>
      <Box display="flex" flexDirection="column" gap={5}>
        {error && events.length > 0 && (
          <Box sx={{ my: 2 }}>
            <ErrorMessage {...error} />
          </Box>
        )}

        <CalendarFilters />

        {events.map((event, index) => (
          <React.Fragment key={event.id}>
            {' '}
            <EventArticle event={event} />
            {index < events.length - 1 && <Divider sx={{ my: 3 }} />}
          </React.Fragment>
        ))}

        <Box ref={sentinelRef} sx={{ height: '20px', mt: 2 }} />

        {isFetchingMore && (
          <Box display="flex" justifyContent="center" my={4}>
            <CircularProgress size={30} />
          </Box>
        )}
      </Box>
    </>
  );
};
