import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { useModalContext } from '../lib/hooks/useModalContext';
import { useTranslation } from 'react-i18next';
import { EventArticle } from '@/entities/Event';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';

export const EventDetailsModal = () => {
  const { t } = useTranslation();
  const modalContext = useModalContext();
  const selectedEvent = modalContext?.selectedEvent;
  const setSelectedEvent = modalContext?.setSelectedEvent;

  const handleClose = () => {
    setSelectedEvent?.(null);
  };

  const isOpen = !!selectedEvent;

  const eventColor = selectedEvent?.color ?? 'transparent';

  return (
    <Modal open={isOpen} onClose={handleClose} aria-labelledby="event-details-modal-title">
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          boxShadow: 24,
          borderRadius: 2,
          width: { xs: '90%', sm: '70%', md: '60%', lg: '50%' },
          maxWidth: { sm: 700, md: 850 },
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          outline: 'none',
          borderTop: `4px solid ${eventColor}`,
        }}
      >
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          sx={{
            p: { xs: 1.5, sm: 2 },
            flexShrink: 0,
          }}
        >
          <Typography
            id="event-details-modal-title"
            variant="h6"
            component="h2"
            sx={{ fontWeight: 500, pl: 1 }}
          >
            {t('calendar.eventDetailsTitle')}
          </Typography>
          <IconButton onClick={handleClose} size="medium" title={t('calendar.closeModal')}>
            <CloseIcon />
          </IconButton>
        </Stack>

        <Box
          sx={{
            flexGrow: 1,
            overflowY: 'auto',
            p: { xs: 2, sm: 3 },
          }}
        >
          {selectedEvent ? <EventArticle event={selectedEvent} /> : isOpen && <LoadingIndicator />}
        </Box>
      </Box>
    </Modal>
  );
};
