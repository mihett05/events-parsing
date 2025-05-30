import { Breakpoint, Container } from '@mui/material';
import Navbar from './Navbar';
import { useAppSelector } from '../store/hooks';
import { useGetMeV1UsersMeGetQuery, useReadUserRolesV1UsersRolesUserIdGetQuery } from '../api/api';

type LayoutProps = {
  children?: React.ReactNode;
  childrenMaxWidth?: Breakpoint;
};

export const Layout: React.FC<LayoutProps> = ({ children, childrenMaxWidth = 'xl' }) => {
  const user = useAppSelector((state) => state.user.user);
  useGetMeV1UsersMeGetQuery(undefined, {
    skip: user !== null,
  });
  useReadUserRolesV1UsersRolesUserIdGetQuery(
    {
      userId: user?.id!,
    },
    {
      skip: user === null,
    },
  );

  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Navbar />
      <Container maxWidth={childrenMaxWidth}>{children}</Container>
    </Container>
  );
};
