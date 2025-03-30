import React from 'react';
// import { Box, Typography, IconButton, Button, Stack } from '@mui/material';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';

interface CalendarHeaderProps {
  currentDate: Date;
  onPrevMonth: () => void;
  onNextMonth: () => void;
  onToday: () => void;
}

export const CalendarHeader: React.FC<CalendarHeaderProps> = ({
  currentDate,
  onPrevMonth,
  onNextMonth,
  onToday,
}) => {
  return (
    <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1} px={1}>
      <Box display="flex" alignItems="center">
        <Button
          variant="outlined"
          size="small"
          onClick={onToday}
          sx={{ textTransform: 'none', mr: 1 }}
        >
          Today
        </Button>
        <IconButton size="small" onClick={onPrevMonth} aria-label="Previous month">
          <ChevronLeftIcon />
        </IconButton>
        <IconButton size="small" onClick={onNextMonth} aria-label="Next month" sx={{ mr: 1 }}>
          <ChevronRightIcon />
        </IconButton>
        <Typography variant="h6" component="h2" sx={{ fontWeight: 500 }}>
          {format(currentDate, 'MMMM yyyy')}
        </Typography>
      </Box>
      <Box></Box>
    </Stack>
  );
};
