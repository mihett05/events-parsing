import { UpdateOrganizationV1OrganizationsOrganizationIdPutApiArg } from '@/shared/api/api';
import { z } from '@/shared/config/i18n';

export const OrganizationSchema = z.object({
  title: z.string().trim().min(1),
});

export const createMapOrganizationToUpdate =
  (organizationId: number) =>
  (
    data: z.infer<typeof OrganizationSchema>,
  ): UpdateOrganizationV1OrganizationsOrganizationIdPutApiArg => ({
    organizationId,
    updateOrganizationModelDto: {
      title: data.title,
    },
  });

export const mapOrganizationErrors = {
  404: () => ({
    title: 'Организация не найдена',
  }),
};
