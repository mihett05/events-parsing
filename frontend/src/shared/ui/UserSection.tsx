import { NavLink as RouterNavLink } from 'react-router';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import AccountCircle from '@mui/icons-material/AccountCircle';
import LoginIcon from '@mui/icons-material/Login';
import { AppPaths } from '@/shared/routes';

interface UserSectionProps {
  isLoggedIn: boolean;
  anchorEl: null | HTMLElement;
  onMenuOpen: (event: React.MouseEvent<HTMLElement>) => void;
  onMenuClose: () => void;
  onProfileClick: () => void;
  onLogout: () => void;
}

const UserSection: React.FC<UserSectionProps> = ({
  isLoggedIn,
  anchorEl,
  onMenuOpen,
  onMenuClose,
  onProfileClick,
  onLogout,
}) => {
  return (
    <>
      {isLoggedIn ? (
        <>
          <IconButton size="large" edge="end" onClick={onMenuOpen} color="inherit">
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
            <MenuItem onClick={onProfileClick}>Profile</MenuItem>
            <MenuItem onClick={onLogout}>Logout</MenuItem>
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
            Log In
          </Button>
          <IconButton
            component={RouterNavLink}
            to={AppPaths.login()}
            sx={{
              display: { xs: 'flex', sm: 'none' },
              ml: 1,
            }}
          >
            <LoginIcon />
          </IconButton>
        </>
      )}
    </>
  );
};

export default UserSection;
