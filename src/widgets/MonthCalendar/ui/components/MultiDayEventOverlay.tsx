import React from 'react';
import { Box, useTheme } from '@mui/material';
import { MultiDayEventLayout } from '../../lib/hooks/useMultiDayEventLayout';
import {
  MULTI_DAY_EVENT_HEIGHT,
  MULTI_DAY_EVENT_VERTICAL_GAP,
  DATE_NUMBER_AREA_HEIGHT,
} from '../../lib/constants';
import { getEventBackgroundColor } from '../../lib/eventUtils';

interface MultiDayEventOverlayProps {
  multiDayLayout: MultiDayEventLayout[];
  cellWidth: number;
  rowHeight: number;
  headerHeight: number;
}

export const MultiDayEventOverlay: React.FC<MultiDayEventOverlayProps> = ({
  multiDayLayout,
  cellWidth,
  rowHeight,
  headerHeight,
}) => {
  const theme = useTheme();

  if (cellWidth <= 0 || rowHeight <= 0) {
    return null;
  }

  return (
    <Box
      sx={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        overflow: 'hidden',
      }}
    >
      {multiDayLayout.map((layoutItem) => {
        const topPosition =
          headerHeight +
          layoutItem.weekIndex * rowHeight +
          DATE_NUMBER_AREA_HEIGHT +
          layoutItem.level * (MULTI_DAY_EVENT_HEIGHT + MULTI_DAY_EVENT_VERTICAL_GAP);

        const leftPosition = layoutItem.startCol * cellWidth;
        const width = layoutItem.span * cellWidth;

        if (width <= 0 || topPosition < headerHeight) return null;

        return (
          <Box
            key={`${layoutItem.event.id}-${layoutItem.weekIndex}`}
            sx={{
              position: 'absolute',
              top: `${topPosition}px`,
              left: `${leftPosition}px`,
              width: `${width}px`,
              height: `${MULTI_DAY_EVENT_HEIGHT}px`,
              backgroundColor: getEventBackgroundColor(layoutItem.event),
              borderRadius: '4px',
              px: 1,
              display: 'flex',
              alignItems: 'center',
              overflow: 'hidden',
              whiteSpace: 'nowrap',
              textOverflow: 'ellipsis',
              fontSize: '0.75rem',
              color: theme.palette.getContrastText(getEventBackgroundColor(layoutItem.event)),
              zIndex: 1,
              cursor: 'pointer',
              pointerEvents: 'auto',
              boxSizing: 'border-box',
              '&:hover': { opacity: 0.9 },
            }}
          >
            {layoutItem.event.title}
          </Box>
        );
      })}
    </Box>
  );
};
