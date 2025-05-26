import { Box, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';

interface ErrorMessageProps {
  messageKey?: string;
  messageOptions?: Record<string, any>;
  defaultMessage?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  messageKey = 'errors.generic',
  messageOptions,
  defaultMessage = 'Произошла ошибка. Пожалуйста, попробуйте позже.',
}) => {
  const { t } = useTranslation();

  const translatedMessage = t(messageKey, defaultMessage, messageOptions);

  return (
    <Box display="flex" alignItems="center" justifyContent="center" minHeight="70vh">
      <Typography color="error" align="center" variant="h6">
        {translatedMessage.toString()}
      </Typography>
    </Box>
  );
};
