import { Box, CircularProgress } from '@mui/material';

export function Loading() {
  return (
    <Box display="flex" justifyContent="center" my={4}>
      <CircularProgress size={30} />
    </Box>
  );
}
