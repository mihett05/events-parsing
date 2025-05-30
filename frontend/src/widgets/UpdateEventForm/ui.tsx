import { EventModel, useUpdateEventV1EventsEventIdPutMutation } from '@/shared/api/api';
import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { createMapEventToUpdate, EventSchema, mapEventErrors } from './schema';
import { FormTextField } from '@/shared/forms';
import { TextareaField } from '@/shared/forms/TextareaField';
import { SubmitField } from '@/shared/forms/SubmitField';

type UpdateEventFormProps = {
  event: EventModel;
};

export function UpdateEventForm({ event }: UpdateEventFormProps) {
  const form = useZodForm(EventSchema, {
    defaultValues: {
      title: event.title,
      description: event.description,
      isVisibleStatus: event.isVisible,
    },
  });
  const [trigger, mutation] = useUpdateEventV1EventsEventIdPutMutation();

  const formMapper = createMapEventToUpdate(event.id);

  return (
    <BaseForm
      config={{
        form,
        trigger,
        mutation,
        formMapper,
        errorMappers: mapEventErrors,
      }}
      title="Редактирование событий"
    >
      <FormTextField name="title" label="Название" />
      <TextareaField name="description" label="Описание" />
      <SubmitField>Сохранить событие</SubmitField>
    </BaseForm>
  );
}
