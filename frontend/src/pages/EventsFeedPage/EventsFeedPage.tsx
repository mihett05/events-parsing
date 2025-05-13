import { Layout } from '@/shared/ui/Layout';
import { EventsFeed } from '@widgets/EventsFeed';
import { useEventsFeedPageController } from './hooks/useEventsFeedPageController';

export const EventsFeedPage = () => {
  const { activeFilters, handleFilterChange } = useEventsFeedPageController();

  return (
    <Layout>
      <EventsFeed activeFilters={activeFilters} onFilterChange={handleFilterChange} />
    </Layout>
  );
};
