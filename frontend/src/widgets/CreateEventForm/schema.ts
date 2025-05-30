import { CreateEventV1EventsPostApiArg } from '@/shared/api/api';
import { z } from '@/shared/config/i18n';

export const CreateEventSchema = z.object({
  title: z.string().trim().min(1),
  type: z.string().trim().min(1),
  format: z.string().trim().min(1),
  location: z.string().trim().min(1),
  description: z.string().trim().min(1),
  endDate: z.date(),
  startDate: z.date(),
  endRegistration: z.date(),
  isVisible: z.boolean(),
});

export const createMapEventToCreate =
  (organizationId: number) =>
  (data: z.infer<typeof CreateEventSchema>): CreateEventV1EventsPostApiArg => ({
    createEventModelDto: {
      organizationId,
      description: data.description,
      title: data.title,
      format: data.format as any,
      type: data.type as any,
      location: data.location,
      endDate: data.endDate.toISOString(),
      startDate: data.endDate.toISOString(),
      endRegistration: data.endDate.toISOString(),
      isVisible: data.isVisible,
    },
  });

export const mapCreateEventErrors = {};
