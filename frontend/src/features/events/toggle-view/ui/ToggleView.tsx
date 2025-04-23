import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import { useMatch, useNavigate } from 'react-router';

import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import FeedIcon from '@mui/icons-material/Feed';

type EventsView = 'feed' | 'calendar';

export const ToggleEventsView = () => {
  const navigate = useNavigate();

  const feedMatch = useMatch('/feed');
  const calendarMatch = useMatch('/');

  const view = feedMatch ? 'feed' : calendarMatch ? 'calendar' : 'feed';

  const handleChange = (_: React.MouseEvent<HTMLElement>, newView: EventsView) => {
    if (newView) {
      navigate(newView === 'feed' ? '/feed' : '/');
    }
  };

  return (
    <ToggleButtonGroup
      value={view}
      exclusive
      onChange={handleChange}
      aria-label="change events view"
    >
      <ToggleButton value="feed">
        <FeedIcon />
      </ToggleButton>
      <ToggleButton value="calendar">
        <CalendarMonthIcon />
      </ToggleButton>
    </ToggleButtonGroup>
  );
};
