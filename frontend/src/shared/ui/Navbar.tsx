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

const Navbar: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(true);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();

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
    <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
      <AppBar
        component="nav"
        position="static"
        sx={{
          boxShadow: 'none',
          backgroundColor: '#fff',
          color: 'text.primary',
        }}
      >
        <Toolbar>
          <IconButton
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
            }}
          >
            IKNT
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <DesktopNavigation />
          <UserSection
            isLoggedIn={isLoggedIn}
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
        isLoggedIn={isLoggedIn}
        onClose={handleDrawerToggle}
        onLogout={handleLogout}
      />
    </Box>
  );
};

export default Navbar;
