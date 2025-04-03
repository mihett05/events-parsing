import { Modal, Box, Typography } from '@mui/material';
import { useModalContext } from '../../lib/hooks/useModalContext';

export const EventDetailsModal: React.FC = () => {
  const { selectedEvent, setSelectedEvent } = useModalContext();

  const handleClose = () => {
    setSelectedEvent(null);
  };

  return (
    <Modal open={!!selectedEvent} onClose={handleClose}>
      <Box
        sx={{
          p: 4,
          backgroundColor: 'white',
          borderRadius: 2,
          maxWidth: 400,
          margin: 'auto',
          mt: '10%',
        }}
      >
        {selectedEvent && (
          <>
            <Typography variant="h6">{selectedEvent.title}</Typography>
            <Typography variant="body1">
              Start Date: {selectedEvent.startDate.toDateString()}
            </Typography>
            {selectedEvent.endDate && (
              <Typography variant="body1">
                End Date: {selectedEvent.endDate.toDateString()}
              </Typography>
            )}
            <Typography variant="body1">Format: {selectedEvent.format}</Typography>
            <Typography variant="body1">Type: {selectedEvent.type}</Typography>
            <Typography gutterBottom variant="subtitle1" sx={{ mt: 2 }}>
              <strong>Description:</strong>
            </Typography>
            <Typography style={{ whiteSpace: 'pre-wrap' }}>{selectedEvent.description}</Typography>
          </>
        )}
      </Box>
    </Modal>
  );
};
