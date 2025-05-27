import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { Box, Button, CircularProgress, Grid, Link, Typography } from '@mui/material';
import { mapUserErrors, mapUserToRequest, UserSchema } from './schema';
import { useAppSelector } from '@/shared/store/hooks';
import {
  useCreateIcalV1EventsSubscribeIcalPostMutation,
  useCreateTelegramLinkV1UsersTelegramPostMutation,
  useUpdateUserV1UsersMePutMutation,
} from '@/shared/api/api';
import { FormTextField } from '@/shared/forms';
import { SelectField } from '@/shared/forms/SelectField';
import { SubmitField } from '@/shared/forms/SubmitField';

export function UserForm() {
  const user = useAppSelector((state) => state.user);

  const form = useZodForm(UserSchema, {
    defaultValues: {
      firstname: user.user?.fullname.split(' ')[0] || '',
      lastname: user.user?.fullname.split(' ')[1] || '',
      middleName: user.user?.fullname.split(' ')[2] || '',
      sendToType: user.user?.settings.type,
    },
  });
  const [trigger, mutation] = useUpdateUserV1UsersMePutMutation();

  // TODO: разделить по features

  const [createIcal, createIcalMutation] = useCreateIcalV1EventsSubscribeIcalPostMutation();

  const icalLink =
    user.user?.settings.calendarUuid || (createIcalMutation.isSuccess && createIcalMutation.data)
      ? `https://api.events.lovepaw.ru/v1/events/subscribe/ical/${user.user?.settings.calendarUuid || createIcalMutation.data}`
      : null;

  const [createTelegram] = useCreateTelegramLinkV1UsersTelegramPostMutation();

  return (
    <Grid container spacing={5}>
      <Grid size={4}>
        <BaseForm
          config={{
            form,
            formMapper: mapUserToRequest,
            errorMappers: mapUserErrors,
            trigger,
            mutation,
          }}
          title="Редактирование информации о пользователе"
        >
          <FormTextField name="lastname" label="Фамилия" />
          <FormTextField name="firstname" label="Имя" />
          <FormTextField name="middleName" label="Отчество" />
          <SelectField
            name="sendToType"
            options={[
              ['EMAIL', 'E-Mail'],
              ['TELEGRAM', 'Telegram'],
            ]}
          />
          <SubmitField>Сохранить</SubmitField>
        </BaseForm>
      </Grid>
      <Grid size={4}>
        <Typography>Подключение внешних календарей</Typography>
        {createIcalMutation.isLoading ? (
          <CircularProgress />
        ) : (
          <>
            {icalLink ? (
              <Typography>
                Ссылка для календаря:{' '}
                <Link
                  href="#"
                  onClick={() => {
                    navigator.clipboard.writeText(icalLink);
                  }}
                >
                  копировать
                </Link>
              </Typography>
            ) : (
              <Button
                onClick={() => {
                  createIcal();
                }}
              >
                Создать ссылка для календаря
              </Button>
            )}
          </>
        )}
      </Grid>
      <Grid size={4}>
        {user.user?.telegramId ? (
          <Typography>Telegram подключён</Typography>
        ) : (
          <Button
            variant="contained"
            onClick={async () => {
              const response = await createTelegram().unwrap();
              if (response) {
                window.open(`https://${response}`);
              }
            }}
          >
            Подключить Telegram
          </Button>
        )}
      </Grid>
    </Grid>
  );
}
