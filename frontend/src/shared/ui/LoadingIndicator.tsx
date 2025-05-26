import { Box, CircularProgress } from '@mui/material';

const LoadingIndicator = () => {
  return (
    <Box display="flex" justifyContent="center" alignItems="center">
      <CircularProgress />
    </Box>
  );
};

export default LoadingIndicator;
