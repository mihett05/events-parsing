import { useRegisterUserV1AuthRegisterPostMutation } from '@/shared/api/api';
import { FormTextField, PasswordTextField } from '@/shared/forms';
import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { RegisterSchema, mapRegisterToRequest, mapRegisterErrors } from './schema';
import { SubmitField } from '@/shared/forms/SubmitField';
import { useState } from 'react';
import { Link, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router';
import { AppPaths } from '@/shared/routes';

export const RegisterForm = () => {
  const [isSuccess, setIsSuccess] = useState(false);
  const { t } = useTranslation('', {
    keyPrefix: 'register',
  });

  const form = useZodForm(RegisterSchema);
  const [trigger, mutation] = useRegisterUserV1AuthRegisterPostMutation();

  if (isSuccess) {
    return (
      <Typography variant="h4" align="center">
        {t('success')}
      </Typography>
    );
  }

  return (
    <BaseForm
      config={{
        form,
        mutation,
        formMapper: mapRegisterToRequest,
        errorMappers: mapRegisterErrors,
        trigger,
      }}
      onSuccess={() => setIsSuccess(true)}
      title={t('title')}
    >
      <FormTextField name="email" label={t('email')} />
      <PasswordTextField name="password" label={t('password')} />
      <PasswordTextField name="confirmPassword" label={t('confirmPassword')} />
      <FormTextField name="lastname" label={t('lastname')} />
      <FormTextField name="firstname" label={t('firstname')} />
      <FormTextField name="middleName" label={t('middleName')} />
      <SubmitField>{t('register')}</SubmitField>
      <Link component={RouterLink} to={AppPaths.login()} align="center">
        или войдите в аккаунт
      </Link>
    </BaseForm>
  );
};
