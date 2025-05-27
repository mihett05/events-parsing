import { useAuthRequired } from '@/shared/hooks/authorization';
import { Layout } from '@/shared/ui/Layout';
import { UserForm } from '@/widgets/UserForm';
import { CircularProgress } from '@mui/material';

export function ProfilePage() {
  const isAuthorized = useAuthRequired();

  return isAuthorized ? (
    <Layout>
      <UserForm />
    </Layout>
  ) : (
    <CircularProgress />
  );
}
