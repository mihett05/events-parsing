import { useReadEventV1EventsEventIdGetQuery } from '@/shared/api/api';
import { Layout } from '@/shared/ui/Layout';
import { Loader } from '@/shared/ui/Loader';
import { UpdateEventForm } from '@/widgets/UpdateEventForm';
import { useParams } from 'react-router';

export function EventEditPage() {
  const { eventId } = useParams<{ eventId: string }>();

  const query = useReadEventV1EventsEventIdGetQuery({
    eventId: parseInt(eventId!),
  });

  return (
    <Layout>
      <Loader query={query}>{(data) => <UpdateEventForm event={data} />}</Loader>
    </Layout>
  );
}
