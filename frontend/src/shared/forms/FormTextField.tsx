import { TextField, TextFieldProps } from '@mui/material';
import { Controller, useFormContext, FieldValues, FieldPath } from 'react-hook-form';

export type FormTextFieldProps<T extends FieldValues> = TextFieldProps & {
  name: FieldPath<T>;
};

export function FormTextField<F extends FieldValues>({ name, ...props }: FormTextFieldProps<F>) {
  const { control } = useFormContext<F>();

  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState: { error } }) => (
        <TextField {...field} {...props} error={error !== undefined} helperText={error?.message} />
      )}
    />
  );
}
