import { useCreateEventV1EventsPostMutation } from '@/shared/api/api';
import { BaseForm, useZodForm } from '@/shared/forms/Form';
import { createMapEventToCreate, CreateEventSchema, mapCreateEventErrors } from './schema';
import { FormTextField } from '@/shared/forms';
import { TextareaField } from '@/shared/forms/TextareaField';
import { SubmitField } from '@/shared/forms/SubmitField';
import { SelectField } from '@/shared/forms/SelectField';
import { FormDateField } from '@/shared/forms/DateField';

type CreateEventFormProps = {
  organizationId: number;
};

export function CreateEventForm({ organizationId }: CreateEventFormProps) {
  const form = useZodForm(CreateEventSchema, {
    defaultValues: {
      isVisible: true,
    },
  });
  const [trigger, mutation] = useCreateEventV1EventsPostMutation();

  const formMapper = createMapEventToCreate(organizationId);

  return (
    <BaseForm
      config={{
        form,
        trigger,
        mutation,
        formMapper,
        errorMappers: mapCreateEventErrors,
      }}
      title="Создание события"
    >
      <FormTextField name="title" label="Название" />
      <TextareaField name="description" label="Описание" />
      <FormTextField name="location" label="Локация" />
      <FormDateField name="startDate" label="Дата начала" />
      <FormDateField name="endDate" label="Дата конца" />
      <FormDateField name="endRegistration" label="Дата конца регистрации" />
      <SelectField
        name="type"
        options={[
          ['Хакатон', 'Хакатон'],
          ['Конференция', 'Конференция'],
          ['Контест', 'Контест'],
          ['Другое', 'Другое'],
        ]}
        label="Тип события"
      />
      <SelectField
        name="format"
        options={[
          ['Дистанционно', 'Дистанционно'],
          ['Очно', 'Очно'],
          ['Смешанное', 'Смешанное'],
          ['Другое', 'Другое'],
        ]}
        label="Формат события"
      />
      <SubmitField>Создать событие</SubmitField>
    </BaseForm>
  );
}
