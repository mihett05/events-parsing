import React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

interface DayNamesHeaderProps {
  dayNames: string[];
  height?: number | string;
}

export const DayNamesHeader: React.FC<DayNamesHeaderProps> = ({ dayNames, height }) => {
  return (
    <Grid
      container
      columns={7}
      sx={{
        borderBottom: '1px solid #eee',
        mb: 0,
        height: height,
        flexShrink: 0,
      }}
    >
      {dayNames.map((dayName, index) => (
        <Grid size={1} key={dayName} sx={{ textAlign: 'right', pr: 1, py: 0.5 }}>
          <Typography
            variant="caption"
            fontWeight="500"
            color={index === 0 || index === 6 ? 'error' : 'text.secondary'}
          >
            {dayName}
          </Typography>
        </Grid>
      ))}
    </Grid>
  );
};
