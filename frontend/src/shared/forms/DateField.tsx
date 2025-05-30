import { DatePicker, DatePickerProps } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import { Controller, FieldPath, FieldValues, useFormContext } from 'react-hook-form';

export type FormDateFieldProps<T extends FieldValues> = DatePickerProps<true> & {
  name: FieldPath<T>;
  label: string;
};

export function FormDateField<F extends FieldValues>({
  label,
  name,
  ...props
}: FormDateFieldProps<F>) {
  const { control } = useFormContext();

  return (
    <Controller
      control={control}
      name={name}
      render={({ field }) => {
        return (
          <DatePicker
            label={label}
            {...field}
            value={field.value ? dayjs(field.value) : null}
            onChange={(value, context) => {
              field.onChange(
                (value && (value.set('h', 12) as dayjs.Dayjs | null))?.toDate(),
                context,
              );
            }}
            {...props}
          />
        );
      }}
    />
  );
}
