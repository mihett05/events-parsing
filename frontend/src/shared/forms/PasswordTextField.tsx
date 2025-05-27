import { IconButton, InputAdornment } from '@mui/material';
import { FieldValues } from 'react-hook-form';
import { FormTextField, FormTextFieldProps } from './FormTextField';
import { useState } from 'react';
import { VisibilityOff } from '@mui/icons-material';
import { Visibility } from '@mui/icons-material';

type PasswordTextFieldProps<T extends FieldValues> = FormTextFieldProps<T>;

export const PasswordTextField: React.FC<PasswordTextFieldProps<FieldValues>> = ({
  name,
  ...props
}) => {
  const [hidden, setHidden] = useState(true);
  const toggleHidden = () => {
    setHidden(!hidden);
  };

  const fieldType = hidden ? 'password' : 'text';

  return (
    <FormTextField
      name={name}
      {...props}
      type={fieldType}
      slotProps={{
        input: {
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={toggleHidden}>
                {hidden ? <Visibility /> : <VisibilityOff />}
              </IconButton>
            </InputAdornment>
          ),
        },
      }}
    />
  );
};
