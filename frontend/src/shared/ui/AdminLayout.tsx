import { AppBar, Box, Button, Drawer, IconButton, Toolbar, Typography } from '@mui/material';
import React, { useState } from 'react';
import MenuIcon from '@mui/icons-material/Menu';

type AdminLayoutProps = {
  listSlot?: React.ReactNode;
};

const AdminLayout: React.FC<AdminLayoutProps> = ({ listSlot }) => {
  const [open, setOpen] = useState(false);

  const onDrawerOpen = () => setOpen(true);
  const onDrawerClose = () => setOpen(false);

  return (
    <Box>
      <AppBar component="nav">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={onDrawerOpen}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
          >
            MUI
          </Typography>
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            <Button  sx={{ color: '#fff' }}>
                О
              </Button>}
          </Box>
        </Toolbar>
      </AppBar>
      <nav>
        <Drawer open={open} onClose={onDrawerClose}>

        </Drawer>
      </nav>
    </Box>
  );
};

export default AdminLayout;
