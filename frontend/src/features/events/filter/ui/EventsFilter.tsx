import { useAppSelector } from '@/shared/store/hooks';
import { Box } from '@mui/material';

type EventsFilterProps = {};

// cock dick blowjob
const EventsFilter: React.FC<EventsFilterProps> = ({}) => {
  const events = useAppSelector((state) => state.events);
  return <Box display="flex"></Box>;
};
