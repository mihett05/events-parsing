import React, { useEffect, useRef } from 'react';
import { EventArticle } from '@/entities/Event';
import { Box, Divider, CircularProgress, Typography, Paper } from '@mui/material';
import { useEventsFeed } from '../lib/hooks';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { CalendarFilters } from '@/features/events/filter/ui/EventsFilter';
import { FilterState } from '@/features/events/slice';
import { useTranslation } from 'react-i18next';

interface EventsFeedProps {
  activeFilters: FilterState;
  onFilterChange: (newFilters: Partial<FilterState>) => void;
}

export const EventsFeed: React.FC<EventsFeedProps> = ({ activeFilters, onFilterChange }) => {
  const { t } = useTranslation();
  const { events, isLoading, isFetchingMore, error, handleLoadMore, currentPage, hasMore } =
    useEventsFeed(activeFilters);

  const observer = useRef<IntersectionObserver | null>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (observer.current) observer.current.disconnect();

    if (hasMore) {
      observer.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !isLoading && !isFetchingMore) {
          handleLoadMore();
        }
      });

      if (sentinelRef.current) {
        observer.current.observe(sentinelRef.current);
      }
    }

    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, [handleLoadMore, isLoading, isFetchingMore, hasMore]);

  if (isLoading && events.length === 0 && currentPage === 0) {
    return <LoadingIndicator />;
  }

  if (error && currentPage === 0 && events.length === 0) {
    return <ErrorMessage defaultMessage={t(error.messageKey, 'Ошибка загрузки ленты')} />;
  }

  return (
    <Box display="flex" flexDirection="column" gap={{ xs: 2, sm: 3, md: 5 }}>
      {error && events.length > 0 && (
        <Paper
          elevation={2}
          sx={{ p: 1, bgcolor: 'error.light', color: 'error.contrastText', mb: 2 }}
        >
          <Typography variant="caption">
            {t(error.messageKey, 'Произошла ошибка при обновлении ленты')}
          </Typography>
        </Paper>
      )}
      <CalendarFilters activeFilters={activeFilters} onFilterChange={onFilterChange} />
      {events.length === 0 && !isLoading && !isFetchingMore && !error && (
        <Typography sx={{ textAlign: 'center', color: 'text.secondary', mt: 4 }}>
          {hasMore ? t('feed.loadingInitial') : t('feed.noEventsFound')}
        </Typography>
      )}
      {events.map((event, index) => (
        <React.Fragment key={event.id}>
          <EventArticle event={event} />
          {index < events.length - 1 && <Divider sx={{ my: { xs: 2, sm: 3 } }} />}
        </React.Fragment>
      ))}

      {hasMore && !isLoading && !isFetchingMore && (
        <Box ref={sentinelRef} sx={{ height: '20px', mt: 2 }} />
      )}
      {isFetchingMore && (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress size={30} />
        </Box>
      )}
      {!hasMore && events.length > 0 && !isFetchingMore && !isLoading && (
        <Typography sx={{ textAlign: 'center', color: 'text.secondary', mt: 4, mb: 2 }}>
          {t('feed.allItemsLoaded')}
        </Typography>
      )}
    </Box>
  );
};
