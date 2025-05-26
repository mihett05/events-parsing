import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import { CalendarEvent } from '../model/types';
import { useModalContext } from '@/widgets/MonthCalendar/lib/hooks/useModalContext';

interface EventItemProps {
  event: CalendarEvent;
}

export const EventItem: React.FC<EventItemProps> = ({ event }) => {
  const modalContext = useModalContext();

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    modalContext?.setSelectedEvent(event);
  };

  return (
    <Stack
      direction="row"
      alignItems="center"
      spacing={0.5}
      sx={{ width: '100%', overflow: 'hidden', mb: '2px', cursor: 'pointer' }}
      onClick={handleClick}
      title={event.title}
    >
      <Box
        component="span"
        sx={{
          width: 8,
          height: 8,
          borderRadius: '50%',
          backgroundColor: event.color,
          flexShrink: 0,
          mr: 0.5,
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
          flexGrow: 1,
        }}
      >
        {event.title}
      </Typography>
    </Stack>
  );
};
