import { AdminNavigation } from '@/features/AdminNavigation';
import { OrganizationModel, useReadAllEventsV1EventsGetQuery } from '@/shared/api/api';
import { AppPaths } from '@/shared/routes';
import { AdminSearchGrid, makeSearchGridHook } from '@/shared/ui/AdminSearchGrid';
import { Badge, Box, Chip, Paper, Typography } from '@mui/material';
import { useNavigate } from 'react-router';

const useEvents = makeSearchGridHook(useReadAllEventsV1EventsGetQuery);

type EventsGrid = {
  organization: OrganizationModel;
};

export function EventsGrid({ organization }: EventsGrid) {
  const navigate = useNavigate();
  const query = useEvents({
    organizationId: organization.id,
  });

  return (
    <Box>
      <AdminNavigation
        context={{
          organization,
        }}
      />
      <AdminSearchGrid
        {...query}
        renderer={(entity) =>
          entity.organizationId && (
            <Paper
              key={`event-${entity.id}`}
              onClick={() => {
                navigate(AppPaths.event(entity.id));
              }}
              sx={{
                cursor: 'pointer',
                p: 2,
              }}
            >
              <Typography>{entity.title}</Typography>
              <Chip label={entity.type} />
              <Chip label={entity.format} />
              <Typography>
                {entity.startDate} | {entity.endDate}
              </Typography>
            </Paper>
          )
        }
        searchGetter={(entity) => entity.title}
      />
    </Box>
  );
}
