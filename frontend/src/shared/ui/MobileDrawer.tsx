import { NavLink as RouterNavLink } from 'react-router';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import { Feed, Login, Logout, AccountBox } from '@mui/icons-material';
import { AppPaths } from '@/shared/routes';
import { useTranslation } from 'react-i18next';

interface MobileDrawerProps {
  isOpen: boolean;
  isLoggedIn: boolean;
  onClose: () => void;
  onLogout: () => void;
}

const MobileDrawer: React.FC<MobileDrawerProps> = ({ isOpen, isLoggedIn, onClose, onLogout }) => {
  const { t } = useTranslation();

  const handleLogoutClick = () => {
    onClose();
    onLogout();
  };

  const activeStyle = {
    backgroundColor: 'action.selected',
    '& .MuiTypography-root, & .MuiSvgIcon-root': {
      fontWeight: 'bold',
    },
  };

  const drawerContent = (
    <Box sx={{ width: 250 }} role="presentation">
      <Typography variant="h6" sx={{ my: 2, textAlign: 'center' }}>
        {t('appName')}
      </Typography>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            component={RouterNavLink}
            to={AppPaths.calendar()}
            onClick={onClose}
            sx={{ '&.active': activeStyle }}
          >
            <ListItemIcon>
              <CalendarMonthIcon />
            </ListItemIcon>
            <ListItemText primary={t('navigation.calendar')} />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            component={RouterNavLink}
            to={AppPaths.eventsFeed()}
            onClick={onClose}
            sx={{ '&.active': activeStyle }}
          >
            <ListItemIcon>
              <Feed />
            </ListItemIcon>
            <ListItemText primary={t('navigation.eventsFeed')} />
          </ListItemButton>
        </ListItem>
        <Divider sx={{ my: 1 }} />
        {isLoggedIn ? (
          <>
            <ListItem disablePadding>
              <ListItemButton
                component={RouterNavLink}
                to={AppPaths.profile()}
                onClick={onClose}
                sx={{ '&.active': activeStyle }}
              >
                <ListItemIcon>
                  <AccountBox />
                </ListItemIcon>
                <ListItemText primary={t('navigation.profile')} />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton onClick={handleLogoutClick}>
                <ListItemIcon>
                  <Logout />
                </ListItemIcon>
                <ListItemText primary={t('navigation.logout')} />
              </ListItemButton>
            </ListItem>
          </>
        ) : (
          <>
            <ListItem disablePadding>
              <ListItemButton
                component={RouterNavLink}
                to={AppPaths.login()}
                onClick={onClose}
                sx={{ '&.active': activeStyle }}
              >
                <ListItemIcon>
                  <Login />
                </ListItemIcon>
                <ListItemText primary={t('navigation.loginRegister')} />
              </ListItemButton>
            </ListItem>
          </>
        )}
      </List>
    </Box>
  );

  return (
    <Box component="nav">
      <Drawer
        variant="temporary"
        open={isOpen}
        onClose={onClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 250 },
        }}
      >
        {drawerContent}
      </Drawer>
    </Box>
  );
};

export default MobileDrawer;
