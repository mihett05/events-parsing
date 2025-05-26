import { Container } from '@mui/material';
import Navbar from './Navbar';

type LayoutProps = {
  children: React.ReactNode;
};

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Navbar />
      {children}
    </Container>
  );
};
