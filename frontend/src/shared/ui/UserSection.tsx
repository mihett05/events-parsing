import { NavLink as RouterNavLink, useNavigate } from 'react-router';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import AccountCircle from '@mui/icons-material/AccountCircle';
import LoginIcon from '@mui/icons-material/Login';
import { AppPaths } from '@/shared/routes';
import { useTranslation } from 'react-i18next';

interface UserSectionProps {
  isLoggedIn: boolean;
  isAdmin: boolean;
  anchorEl: null | HTMLElement;
  onMenuOpen: (event: React.MouseEvent<HTMLElement>) => void;
  onMenuClose: () => void;
  onProfileClick: () => void;
  onLogout: () => void;
}

const UserSection: React.FC<UserSectionProps> = ({
  isLoggedIn,
  isAdmin,
  anchorEl,
  onMenuOpen,
  onMenuClose,
  onProfileClick,
  onLogout,
}) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  console.log(isAdmin);

  return (
    <>
      {isLoggedIn ? (
        <>
          <IconButton size="large" onClick={onMenuOpen} color="inherit" edge="end">
            <AccountCircle />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            keepMounted
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={Boolean(anchorEl)}
            onClose={onMenuClose}
          >
            <MenuItem onClick={onProfileClick}>{t('navigation.profile')}</MenuItem>
            {isAdmin && (
              <MenuItem onClick={() => navigate(AppPaths.organizations())}>
                {t('navigation.admin')}
              </MenuItem>
            )}
            <MenuItem onClick={onLogout}>{t('navigation.logout')}</MenuItem>
          </Menu>
        </>
      ) : (
        <>
          <Button
            component={RouterNavLink}
            to={AppPaths.login()}
            sx={{
              display: { xs: 'none', sm: 'block' },
              ml: 1,
              color: 'inherit',
              '&.active': {
                textDecoration: 'underline',
              },
            }}
          >
            {t('navigation.login')}
          </Button>
          <Box sx={{ display: { xs: 'flex', sm: 'none' } }}>
            {' '}
            <IconButton
              component={RouterNavLink}
              to={AppPaths.login()}
              color="inherit"
              sx={{ ml: 1 }}
            >
              <LoginIcon />
            </IconButton>
          </Box>
        </>
      )}
    </>
  );
};

export default UserSection;
