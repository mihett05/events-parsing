import { Box, Chip, Typography } from '@mui/material';
import { CalendarEvent } from '../model/types';

type EventArticleProps = {
  event: CalendarEvent;
  ref?: React.RefObject<HTMLDivElement> | null;
};

export const EventArticle: React.FC<EventArticleProps> = ({ event, ref }) => {
  return (
    <Box ref={ref}>
      <Typography variant="h5">{event.title}</Typography>
      <Box display="flex" gap={1}>
        <Chip label={event.type} />
        <Chip label={event.format} />
      </Box>
      <Typography variant="body1">
        {event.startDate.toLocaleDateString()} {event.endDate ? '-' : ''}{' '}
        {event.endDate?.toLocaleDateString()}
      </Typography>
      <Typography variant="body1">
        {event.endRegistration && `Регистрация до ${event.endRegistration.toLocaleDateString()}`}
      </Typography>
      <Typography variant="body1">{event.description}</Typography>
      <Box
        sx={{
          width: '100%',
          height: '100px',
          background: generateTitleGradient(event.title),
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography variant="h4" color="white">
          {event.title}
        </Typography>
      </Box>
    </Box>
  );
};

/**
 * Генерация градиентного фона исходя из названия события
 * Насыщенность и освещение выбираются контрастно белому
 * @param title - Название события
 * @returns CSS (linear-gradient) градиентный фон
 */
function generateTitleGradient(title: string) {
  const hash = stringToHash(title);

  const hue1 = Math.abs(hash % 360);
  const saturation = 70 + Math.abs(hash % 30);
  const lightness = 40 + Math.abs(hash % 20);

  const hue2 = (hue1 + 120) % 360;

  return `linear-gradient(135deg, 
        hsl(${hue1}, ${saturation}%, ${lightness}%), 
        hsl(${hue2}, ${saturation}%, ${lightness}%))`;
}

function stringToHash(str: string) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return hash;
}
