import { Container } from '@mui/material';

type LayoutProps = {
  children: React.ReactNode;
};

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      {children}
    </Container>
  );
};
