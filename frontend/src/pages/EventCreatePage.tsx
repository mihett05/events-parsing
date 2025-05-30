import { Layout } from '@/shared/ui/Layout';
import { CreateEventForm } from '@/widgets/CreateEventForm';
import { useParams } from 'react-router';

export function EventCreatePage() {
  const { organizationId } = useParams<{ organizationId: string }>();

  return (
    <Layout>
      <CreateEventForm organizationId={parseInt(organizationId!)} />
    </Layout>
  );
}
