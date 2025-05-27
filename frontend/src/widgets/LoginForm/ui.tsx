import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { LoginSchema, mapLoginErrors, mapLoginToRequest } from './schema';
import { api, useLoginUserV1AuthLoginPostMutation } from '@/shared/api/api';
import { FormTextField, PasswordTextField } from '@/shared/forms';
import { useTranslation } from 'react-i18next';
import { SubmitField } from '@/shared/forms/SubmitField';
import { Link } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router';
import { AppPaths } from '@/shared/routes';
import { useAppDispatch } from '@/shared/store/hooks';

export function LoginForm() {
  const { t } = useTranslation('', {
    keyPrefix: 'login',
  });
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const form = useZodForm(LoginSchema);
  const [trigger, mutation] = useLoginUserV1AuthLoginPostMutation();

  return (
    <BaseForm
      config={{
        form,
        formMapper: mapLoginToRequest,
        errorMappers: mapLoginErrors,
        mutation,
        trigger,
      }}
      title={t('title')}
      onSuccess={(response) => {
        dispatch(
          api.endpoints.readUserRolesV1UsersRolesUserIdGet.initiate({
            userId: response.user.id,
          }),
        );
        navigate(AppPaths.profile());
      }}
    >
      <FormTextField name="email" label={t('email')} />
      <PasswordTextField name="password" label={t('password')} />
      <SubmitField>{t('login')}</SubmitField>
      <Link component={RouterLink} to={AppPaths.register()} align="center">
        или создайте аккаунт
      </Link>
    </BaseForm>
  );
}
