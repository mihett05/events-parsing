import { useReadOrganizationV1OrganizationsOrganizationIdGetQuery } from '@/shared/api/api';
import { Layout } from '@/shared/ui/Layout';
import { Loader } from '@/shared/ui/Loader';
import { OrganizationInfo } from '@/widgets/OrganizationInfo';
import { useParams } from 'react-router';

export function OrganizationPage() {
  const params = useParams<{ organizationId: string }>();

  const query = useReadOrganizationV1OrganizationsOrganizationIdGetQuery({
    organizationId: parseInt(params.organizationId!),
  });

  return (
    <Layout>
      <Loader query={query}>{(data) => <OrganizationInfo organization={data} />}</Loader>
    </Layout>
  );
}
