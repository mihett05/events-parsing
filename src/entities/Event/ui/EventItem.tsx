import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import { CalendarEvent } from '../model/types';

interface EventItemProps {
  event: CalendarEvent;
}

const eventColorMapping: { [key: string]: string } = {
  orange: '#ff9800',
  red: '#f44336',
  green: '#4caf50',
  blue: '#2196f3',
  lightgreen: '#69f0ae',
};

export const EventItem: React.FC<EventItemProps> = ({ event }) => {
  const dotColor = eventColorMapping[event.color.toLowerCase()] || event.color;

  return (
    <Stack
      direction="row"
      alignItems="center"
      spacing={0.5}
      sx={{ width: '100%', overflow: 'hidden', mb: '2px' }}
    >
      <Box
        component="span"
        sx={{
          width: 8,
          height: 8,
          borderRadius: '50%',
          backgroundColor: dotColor,
          flexShrink: 0,
        }}
      />
      <Typography
        variant="caption"
        component="div"
        sx={{
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          lineHeight: 1.2,
          fontSize: '0.7rem',
        }}
      >
        {event.title}
      </Typography>
    </Stack>
  );
};
