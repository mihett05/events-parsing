import { EventArticle } from '@/entities/Event';
import { Box, Divider, CircularProgress } from '@mui/material';
import { useEventsFeed } from '../lib/hooks';
import { useEffect, useRef } from 'react';
import { ToggleEventsView } from '@features/events/toggle-view';
export const EventsFeed = () => {
  const { events, isLoading, error, handleLoadMore } = useEventsFeed();

  const observer = useRef<IntersectionObserver | null>(null);

  const sentinelIndex = events.length - 5;
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

  return (
    <>
      <Box display="flex" justifyContent="flex-end">
        <ToggleEventsView />
      </Box>
      <Box display="flex" flexDirection="column" gap={5} onScroll={handleLoadMore}>
        {events.map((event, index) => (
          <>
            <EventArticle
              key={`event-${event.id}`}
              event={event}
              ref={index === sentinelIndex ? sentinelRef : null}
            />
            {index !== events.length - 1 && <Divider />}
          </>
        ))}
        {isLoading && <CircularProgress />}
      </Box>
    </>
  );
};
