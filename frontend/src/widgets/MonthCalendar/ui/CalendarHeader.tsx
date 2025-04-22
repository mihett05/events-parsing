import React from 'react';
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
  const formattedDate = format(currentDate, 'MMMM yyyy');

  return (
    <Stack
      direction="row"
      justifyContent="space-between"
      alignItems="center"
      mb={1}
      px={{ xs: 1, sm: 2 }}
      py={0.5}
      sx={{ borderBottom: '1px solid #eee', flexShrink: 0 }}
    >
      <Box display="flex" alignItems="center">
        <Button
          variant="outlined"
          size="small"
          onClick={onToday}
          sx={{ textTransform: 'none', mr: 1 }}
          aria-label="Go to Today"
        >
          Today
        </Button>
        <IconButton
          size="small"
          onClick={onPrevMonth}
          aria-label="Previous month"
          title="Previous month"
        >
          <ChevronLeftIcon />
        </IconButton>
        <IconButton
          size="small"
          onClick={onNextMonth}
          aria-label="Next month"
          title="Next month"
          sx={{ mr: 1 }}
        >
          <ChevronRightIcon />
        </IconButton>
      </Box>

      <Typography variant="h6" component="h2" sx={{ fontWeight: 500, textAlign: 'center' }}>
        {formattedDate}
      </Typography>
    </Stack>
  );
};
