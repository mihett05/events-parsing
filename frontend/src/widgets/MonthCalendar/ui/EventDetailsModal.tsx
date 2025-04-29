import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Modal from '@mui/material/Modal';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { format, isValid, isSameDay } from 'date-fns';
import { useModalContext } from '../lib/hooks/useModalContext';

export const EventDetailsModal: React.FC = () => {
  const { selectedEvent, setSelectedEvent } = useModalContext()!;

  const handleClose = () => {
    setSelectedEvent(null);
  };

  const isOpen = !!selectedEvent;

  return (
    <Modal open={isOpen} onClose={handleClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          boxShadow: 24,
          borderRadius: 2,
          p: { xs: 2, sm: 3 },
          width: { xs: '90%', sm: 400, md: 500 },
          maxWidth: '95vw',
          maxHeight: '85vh',
          overflowY: 'auto',
          outline: 'none',
        }}
      >
        {selectedEvent && (
          <>
            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography
                id="event-details-title"
                variant="h6"
                component="h2"
                sx={{ wordBreak: 'break-word' }}
              >
                {selectedEvent.title}
              </Typography>
              <IconButton
                aria-label="close event details"
                onClick={handleClose}
                size="small"
                title="Close"
              >
                <CloseIcon />
              </IconButton>
            </Stack>

            <Divider sx={{ mb: 2 }} />

            <Stack spacing={1.5}>
              {' '}
              <Typography variant="body1">
                <strong>Start:</strong> {format(selectedEvent.startDate, 'PPp')}
              </Typography>
              {selectedEvent.endDate &&
                isValid(selectedEvent.endDate) &&
                !isSameDay(selectedEvent.startDate, selectedEvent.endDate) && (
                  <Typography variant="body1">
                    <strong>End:</strong> {format(selectedEvent.endDate, 'PPp')}
                  </Typography>
                )}
              <Typography variant="body1">
                <strong>Format:</strong> {selectedEvent.format}
              </Typography>
              <Typography variant="body1">
                <strong>Type:</strong> {selectedEvent.type}
              </Typography>
              {selectedEvent.description && String(selectedEvent.description).trim() && (
                <>
                  <Typography variant="subtitle1" sx={{ mt: 2, fontWeight: 'bold' }}>
                    Description:
                  </Typography>
                  <Box
                    sx={{
                      maxHeight: '25vh',
                      overflowY: 'auto',
                      pl: 1,
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word',
                    }}
                    id="event-details-description"
                  >
                    <Typography variant="body2">{selectedEvent.description}</Typography>
                  </Box>
                </>
              )}
            </Stack>
          </>
        )}
        {!selectedEvent && isOpen && <Typography>Loading event details...</Typography>}
      </Box>
    </Modal>
  );
};
