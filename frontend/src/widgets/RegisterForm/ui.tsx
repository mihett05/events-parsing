import { useRegisterUserV1AuthRegisterPostMutation } from '@/shared/api/api';
import { FormTextField } from '@/shared/forms';
import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { RegisterSchema, mapRegisterToRequest, mapRegisterErrors } from './schema';
import { SubmitField } from '@/shared/forms/SubmitField';

export const RegisterForm = () => {
  const form = useZodForm(RegisterSchema);
  const [trigger, mutation] = useRegisterUserV1AuthRegisterPostMutation();

  return (
    <BaseForm
      config={{
        form,
        mutation,
        formMapper: mapRegisterToRequest,
        errorMappers: mapRegisterErrors,
        trigger,
      }}
      title="Регистрация"
    >
      <FormTextField name="email" label="Email" />
      <FormTextField name="password" label="Пароль" />
      <FormTextField name="confirmPassword" label="Повторите пароль" />
      <SubmitField>Создать аккаунт</SubmitField>
    </BaseForm>
  );
};
