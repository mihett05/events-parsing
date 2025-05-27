import {
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
  SelectProps,
} from '@mui/material';
import { FieldPath, FieldValues, useController, useFormContext } from 'react-hook-form';

export type SelectFieldProps<T extends FieldValues> = SelectProps & {
  name: FieldPath<T>;
  options: [string, string][];
  defaultValue?: string;
};

export function SelectField<F extends FieldValues>({
  name,
  label,
  options,
  defaultValue,
  ...props
}: SelectFieldProps<F>) {
  const { control } = useFormContext();
  const {
    field,
    fieldState: { error },
  } = useController({ control, name });

  return (
    <FormControl error={error !== undefined} fullWidth>
      <InputLabel id={`${name}-label`}>{label}</InputLabel>
      <Select
        defaultValue={defaultValue}
        labelId={`${name}-label`}
        {...field}
        value={field.value ?? ''}
        onChange={(event) => {
          field.onChange(event);
        }}
        label={label}
        {...props}
      >
        {options.map(([optionValue, option]) => (
          <MenuItem value={optionValue} key={optionValue}>
            {option}
          </MenuItem>
        ))}
      </Select>
      {error && <FormHelperText>{error.message}</FormHelperText>}
    </FormControl>
  );
}
