import { useState } from 'react';
import { NavLink as RouterNavLink, useNavigate } from 'react-router';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import DesktopNavigation from './DesktopNavigation';
import UserSection from './UserSection';
import MobileDrawer from './MobileDrawer';
import { AppPaths } from '@/shared/routes';
import { useTranslation } from 'react-i18next';
import { useAppSelector } from '../store/hooks';
import { adminRoles } from '@/entities/User/model/roles';

const Navbar: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.user);

  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(true);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleMenuClose = () => {
    setAnchorEl(null);
  };
  const handleDrawerToggle = () => {
    setMobileOpen((prevState) => !prevState);
  };
  const handleProfileClick = () => {
    handleMenuClose();
    navigate(AppPaths.profile());
  };
  const handleLogout = () => {
    handleMenuClose();
    setMobileOpen(false);
    setIsLoggedIn(false);
    navigate(AppPaths.calendar());
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, mb: 2 }}>
      {' '}
      <AppBar
        component="nav"
        position="static"
        sx={{
          boxShadow: 'none',
          borderBottom: '1px solid #eee',
          backgroundColor: 'background.paper',
          color: 'text.primary',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            component={RouterNavLink}
            to={AppPaths.calendar()}
            sx={{
              flexGrow: 1,
              color: 'inherit',
              textDecoration: 'none',
              display: { xs: 'none', sm: 'block' },
              '&:hover': {
                textDecoration: 'none',
              },
            }}
          >
            {t('appName')}
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'block', sm: 'none' } }} />
          <DesktopNavigation />
          <UserSection
            isLoggedIn={user.user !== null}
            isAdmin={user.organizations.some((role) => adminRoles.includes(role.role))}
            anchorEl={anchorEl}
            onMenuOpen={handleMenuOpen}
            onMenuClose={handleMenuClose}
            onProfileClick={handleProfileClick}
            onLogout={handleLogout}
          />
        </Toolbar>
      </AppBar>
      <MobileDrawer
        isOpen={mobileOpen}
        isLoggedIn={user.user !== null}
        isAdmin={user.organizations.some((role) => adminRoles.includes(role.role))}
        onClose={handleDrawerToggle}
        onLogout={handleLogout}
      />
    </Box>
  );
};

export default Navbar;
