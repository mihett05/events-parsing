import { NavLink as RouterNavLink } from 'react-router';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { AppPaths } from '@/shared/routes';

const DesktopNavigation: React.FC = () => {
  return (
    <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
      <Button
        component={RouterNavLink}
        to={AppPaths.calendar()}
        sx={{
          color: 'inherit',
          mx: 1,
          '&.active': {
            textDecoration: 'underline',
          },
        }}
      >
        Calendar
      </Button>
      <Button
        component={RouterNavLink}
        to={AppPaths.eventsFeed()}
        sx={{
          color: 'inherit',
          mx: 1,
          '&.active': {
            textDecoration: 'underline',
          },
        }}
      >
        Events Feed
      </Button>
    </Box>
  );
};

export default DesktopNavigation;
