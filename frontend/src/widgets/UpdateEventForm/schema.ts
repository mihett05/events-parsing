import { UpdateEventV1EventsEventIdPutApiArg } from '@/shared/api/api';
import { z } from '@/shared/config/i18n';

export const EventSchema = z.object({
  title: z.string().trim().min(1),
  description: z.string().trim().min(1),
  isVisibleStatus: z.boolean(),
});

export const createMapEventToUpdate =
  (eventId: number) =>
  (data: z.infer<typeof EventSchema>): UpdateEventV1EventsEventIdPutApiArg => ({
    eventId,
    updateEventModelDto: {
      description: data.description,
      title: data.title,
      isVisibleStatus: data.isVisibleStatus,
    },
  });

export const mapEventErrors = {
  404: () => ({
    title: 'Событие не найдено',
  }),
};
