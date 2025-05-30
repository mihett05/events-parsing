import {
  OrganizationModel,
  useUpdateOrganizationV1OrganizationsOrganizationIdPutMutation,
} from '@/shared/api/api';
import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { Box, Divider, Typography } from '@mui/material';
import { OrganizationSchema, createMapOrganizationToUpdate, mapOrganizationErrors } from './schema';
import { AdminNavigation } from '@/features/AdminNavigation';
import { FormTextField } from '@/shared/forms';
import { SubmitField } from '@/shared/forms/SubmitField';
import { EventsGrid } from '../EventsGrid';

type OrganizationInfoProps = {
  organization: OrganizationModel;
};

export function OrganizationInfo({ organization }: OrganizationInfoProps) {
  const form = useZodForm(OrganizationSchema, {
    defaultValues: {
      title: organization.title,
    },
  });
  const [trigger, mutation] = useUpdateOrganizationV1OrganizationsOrganizationIdPutMutation();

  const formMapper = createMapOrganizationToUpdate(organization.id);

  return (
    <Box>
      <AdminNavigation
        context={{
          organization,
        }}
      />
      <BaseForm
        config={{
          trigger,
          mutation,
          form,
          formMapper,
          errorMappers: mapOrganizationErrors,
        }}
        title="Организация"
      >
        <FormTextField name="title" label="Название" />
        <SubmitField>Сохранить</SubmitField>
      </BaseForm>
      <Divider
        sx={{
          my: 5,
        }}
      />
      <Box>
        <Typography variant="h5">События организации</Typography>
        <EventsGrid organization={organization} />
      </Box>
    </Box>
  );
}
