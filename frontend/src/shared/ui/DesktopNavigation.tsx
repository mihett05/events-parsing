import { NavLink as RouterNavLink } from 'react-router';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { AppPaths } from '@/shared/routes';
import { useTranslation } from 'react-i18next';

const DesktopNavigation: React.FC = () => {
  const { t } = useTranslation();

  const commonButtonStyles = {
    color: 'inherit',
    mx: 1,
    '&.active': {
      textDecoration: 'underline',
      fontWeight: 'bold',
    },
  };

  return (
    <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
      <Button component={RouterNavLink} to={AppPaths.calendar()} sx={commonButtonStyles}>
        {t('navigation.calendar')}
      </Button>
      <Button component={RouterNavLink} to={AppPaths.eventsFeed()} sx={commonButtonStyles}>
        {t('navigation.eventsFeed')}
      </Button>
    </Box>
  );
};

export default DesktopNavigation;
