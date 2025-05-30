import { AdminNavigation } from '@/features/AdminNavigation';
import { useReadAllOrganizationsV1OrganizationsGetQuery } from '@/shared/api/api';
import { AppPaths } from '@/shared/routes';
import { AdminSearchGrid, makeSearchGridHook } from '@/shared/ui/AdminSearchGrid';
import { Box, Paper, Typography } from '@mui/material';
import { useNavigate } from 'react-router';

const useOrganizations = makeSearchGridHook(useReadAllOrganizationsV1OrganizationsGetQuery);

export function OrganizationsGrid() {
  const navigate = useNavigate();
  const query = useOrganizations();

  return (
    <Box>
      <AdminNavigation />
      <AdminSearchGrid
        {...query}
        renderer={(entity) => (
          <Paper
            key={`organization-${entity.id}`}
            onClick={() => {
              navigate(AppPaths.organization(entity.id));
            }}
            sx={{
              cursor: 'pointer',
            }}
          >
            <Typography>{entity.title}</Typography>
          </Paper>
        )}
        searchGetter={(entity) => entity.title}
      />
    </Box>
  );
}
