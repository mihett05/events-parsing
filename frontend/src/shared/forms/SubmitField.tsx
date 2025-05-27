import { Button } from '@mui/material';

type SubmitFieldProps = {
  children?: React.ReactNode;
};

export function SubmitField({ children = 'Отправить' }: SubmitFieldProps) {
  return <Button type="submit">{children}</Button>;
}
