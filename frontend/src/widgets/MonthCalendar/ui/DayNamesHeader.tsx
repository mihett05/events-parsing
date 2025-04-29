import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

interface DayNamesHeaderProps {
  dayNames: string[];
}

export const DayNamesHeader: React.FC<DayNamesHeaderProps> = ({ dayNames }) => {
  return (
    <Box
      display="flex"
      sx={{
        borderBottom: '1px solid #eee',
        py: 0.5,
        px: { xs: 0, sm: 1 },
        flexShrink: 0,
        backgroundColor: '#f9f9f9',
      }}
    >
      {dayNames.map((dayName, index) => (
        <Box
          key={dayName}
          sx={{
            flex: 1,
            textAlign: 'right',
            pr: 1,
          }}
        >
          <Typography
            variant="caption"
            fontWeight="500"
            color={index === 0 || index === 6 ? 'error.main' : 'text.secondary'}
            sx={{
              textTransform: 'uppercase',
              fontSize: '0.7rem',
              display: 'block',
            }}
          >
            {dayName}
          </Typography>
        </Box>
      ))}
    </Box>
  );
};
