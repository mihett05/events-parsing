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

interface MobileDrawerProps {
  isOpen: boolean;
  isLoggedIn: boolean;
  onClose: () => void;
  onLogout: () => void;
}

const MobileDrawer: React.FC<MobileDrawerProps> = ({ isOpen, isLoggedIn, onClose, onLogout }) => {
  const handleLogoutClick = () => {
    onClose();
    onLogout();
  };

  const handleNavigationClick = () => {
    onClose();
  };

  const drawerContent = (
    <Box sx={{ width: 250 }} role="presentation">
      <Typography variant="h6" sx={{ my: 2, textAlign: 'center' }}>
        IKNT
      </Typography>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            component={RouterNavLink}
            to={AppPaths.calendar()}
            onClick={handleNavigationClick}
            sx={{
              '&.active': {
                backgroundColor: 'action.selected',
                '& .MuiTypography-root, & .MuiSvgIcon-root': {
                  fontWeight: 'bold',
                },
              },
            }}
          >
            <ListItemIcon>
              <CalendarMonthIcon />
            </ListItemIcon>
            <ListItemText primary="Calendar" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton
            component={RouterNavLink}
            to={AppPaths.eventsFeed()}
            onClick={handleNavigationClick}
            sx={{
              '&.active': {
                '& .MuiTypography-root, & .MuiSvgIcon-root': {
                  fontWeight: 'bold',
                },
              },
            }}
          >
            <ListItemIcon>
              <Feed />
            </ListItemIcon>
            <ListItemText primary="Events Feed" />
          </ListItemButton>
        </ListItem>

        <Divider sx={{ my: 1 }} />

        {isLoggedIn ? (
          <>
            <ListItem disablePadding>
              <ListItemButton
                component={RouterNavLink}
                to={AppPaths.profile()}
                onClick={handleNavigationClick}
                sx={{
                  '&.active': {
                    '& .MuiTypography-root, & .MuiSvgIcon-root': {
                      fontWeight: 'bold',
                    },
                  },
                }}
              >
                <ListItemIcon>
                  <AccountBox />
                </ListItemIcon>
                <ListItemText primary="Profile" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton onClick={handleLogoutClick}>
                <ListItemIcon>
                  <Logout />
                </ListItemIcon>
                <ListItemText primary="Logout" />
              </ListItemButton>
            </ListItem>
          </>
        ) : (
          <>
            <ListItem disablePadding>
              <ListItemButton
                component={RouterNavLink}
                to={AppPaths.login()}
                onClick={handleNavigationClick}
                sx={{
                  '&.active': {
                    '& .MuiTypography-root, & .MuiSvgIcon-root': {
                      fontWeight: 'bold',
                    },
                  },
                }}
              >
                <ListItemIcon>
                  <Login />
                </ListItemIcon>
                <ListItemText primary="Log In / Register" />
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
