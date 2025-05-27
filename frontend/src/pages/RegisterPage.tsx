import { useAuthProhibited } from '@/shared/hooks/authorization';
import { Layout } from '@/shared/ui/Layout';
import { RegisterForm } from '@/widgets/RegisterForm';

export function RegisterPage() {
  useAuthProhibited();
  return (
    <Layout childrenMaxWidth="md">
      <RegisterForm />
    </Layout>
  );
}
