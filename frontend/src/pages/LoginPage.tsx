import { useAuthProhibited } from '@/shared/hooks/authorization';
import { Layout } from '@/shared/ui/Layout';
import { LoginForm } from '@/widgets/LoginForm';

export function LoginPage() {
  useAuthProhibited();
  return (
    <Layout childrenMaxWidth="md">
      <LoginForm />
    </Layout>
  );
}
