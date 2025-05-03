import { TextField, TextFieldProps } from '@mui/material';
import { Controller, useFormContext, FieldValues, FieldPath } from 'react-hook-form';

export type FormTextFieldProps<T extends FieldValues> = TextFieldProps & {
  name: FieldPath<T>;
};

export const FormTextField: React.FC<FormTextFieldProps<FieldValues>> = ({ name, ...props }) => {
  const { control } = useFormContext();

  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState: { error } }) => (
        <TextField {...field} {...props} error={error !== undefined} helperText={error?.message} />
      )}
    />
  );
};
