import { useState, useEffect, RefObject } from 'react';
import { ESTIMATED_DAY_NAMES_HEADER_HEIGHT } from '../constants';

interface GridDimensions {
  cellWidth: number;
  rowHeight: number;
  headerHeight: number;
  gridHeight: number;
  gridWidth: number;
}

export const useGridDimensions = (
  gridRef: RefObject<HTMLElement>,
  dependencies: unknown[] = [],
): GridDimensions => {
  const [dimensions, setDimensions] = useState<GridDimensions>({
    cellWidth: 0,
    rowHeight: 0,
    headerHeight: ESTIMATED_DAY_NAMES_HEADER_HEIGHT,
    gridHeight: 0,
    gridWidth: 0,
  });

  useEffect(() => {
    const calculateDimensions = () => {
      if (gridRef.current) {
        const rect = gridRef.current.getBoundingClientRect();
        const currentGridWidth = rect.width;
        const currentGridHeight = rect.height;
        const currentHeaderHeight = ESTIMATED_DAY_NAMES_HEADER_HEIGHT;
        if (currentGridWidth > 0 && currentGridHeight > currentHeaderHeight) {
          setDimensions({
            cellWidth: currentGridWidth / 7,
            rowHeight: (currentGridHeight - currentHeaderHeight) / 6,
            headerHeight: currentHeaderHeight,
            gridHeight: currentGridHeight,
            gridWidth: currentGridWidth,
          });
        } else {
          setDimensions((prev) => ({
            ...prev,
            cellWidth: 0,
            rowHeight: 0,
            gridWidth: 0,
            gridHeight: 0,
          }));
        }
      }
    };

    calculateDimensions();

    const handleResize = () => calculateDimensions();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [gridRef, ...dependencies]);

  return dimensions;
};
