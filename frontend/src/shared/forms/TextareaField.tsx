import { FormControl, FormHelperText, InputLabel, TextField, TextFieldProps } from '@mui/material';
import { FieldPath, FieldValues, useController, useFormContext } from 'react-hook-form';

export type TextareaFieldProps<T extends FieldValues> = TextFieldProps & {
  name: FieldPath<T>;
  label?: string;
  defaultValue?: string;
};

export function TextareaField<F extends FieldValues>({
  name,
  label,
  defaultValue,
  ...props
}: TextareaFieldProps<F>) {
  const { control } = useFormContext();
  const {
    field,
    fieldState: { error },
  } = useController({ control, name });

  return (
    <FormControl error={!!error} fullWidth>
      {label && (
        <InputLabel shrink htmlFor={name}>
          {label}
        </InputLabel>
      )}
      <TextField
        id={name}
        multiline
        minRows={4}
        defaultValue={defaultValue}
        {...field}
        value={field.value ?? ''}
        onChange={(event) => field.onChange(event)}
        label={label}
        error={!!error}
        {...props}
      />
      {error && <FormHelperText>{error.message}</FormHelperText>}
    </FormControl>
  );
}
