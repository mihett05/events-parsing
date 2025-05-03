import { FormTextField } from '@/shared/forms';
import { useForm } from 'react-hook-form';

export const RegisterForm = () => {
  const { handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormTextField name="email" label="Email" />
      <FormTextField name="password" label="Password" />
      <FormTextField name="confirmPassword" label="Confirm Password" />
    </form>
  );
};
