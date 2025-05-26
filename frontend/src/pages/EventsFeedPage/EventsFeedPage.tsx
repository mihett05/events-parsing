import { Layout } from '@/shared/ui/Layout';
import { EventsFeed } from '@widgets/EventsFeed';
import { useEventsFeedPageController } from './hooks/useEventsFeedPageController';
import { useMemo } from 'react';

export const EventsFeedPage = () => {
  const { activeFilters, handleFilterChange } = useEventsFeedPageController();
  const feedKey = useMemo(() => {
    return `feed-${activeFilters.type || 'all'}-${activeFilters.format || 'all'}-${activeFilters.organizationId || 'all'}`;
  }, [activeFilters]);

  return (
    <Layout>
      <EventsFeed key={feedKey} activeFilters={activeFilters} onFilterChange={handleFilterChange} />
    </Layout>
  );
};
