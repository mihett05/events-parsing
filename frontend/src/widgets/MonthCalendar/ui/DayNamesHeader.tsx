import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { Theme } from '@mui/material';

interface DayNamesHeaderProps {
  dayNames: string[];
}

export const DayNamesHeader: React.FC<DayNamesHeaderProps> = React.memo(({ dayNames }) => {
  const isWeekend = (index: number): boolean => {
    return index === 5 || index === 6;
  };

  return (
    <Box
      display="flex"
      sx={(theme: Theme) => ({
        borderBottom: `1px solid ${theme.palette.divider}`,
        py: 0.5,
        px: { xs: 0.5, sm: 1 },
        flexShrink: 0,
        backgroundColor: theme.palette.mode === 'light' ? '#f9f9f9' : theme.palette.grey[800],
      })}
    >
      {dayNames.map((dayName, index) => (
        <Box
          key={`${dayName}-${index}`}
          sx={{
            flex: 1,
            textAlign: 'right',
            pr: { xs: 0.5, sm: 1.5 },
          }}
        >
          <Typography
            variant="caption"
            fontWeight="500"
            color={isWeekend(index) ? 'error.main' : 'text.secondary'}
            sx={{
              textTransform: 'uppercase',
              fontSize: '0.65rem',
              userSelect: 'none',
              display: 'block',
            }}
          >
            {dayName}
          </Typography>
        </Box>
      ))}
    </Box>
  );
});
