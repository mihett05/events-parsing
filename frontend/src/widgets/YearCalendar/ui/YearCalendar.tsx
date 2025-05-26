import React from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { useCalendarViewData } from '@/features/events/hooks/useCalendarViewData';
import { YearCalendarHeader } from './YearCalendarHeader';
import { YearCalendarGrid } from './YearCalendarGrid';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { CalendarControlProps } from '@/widgets/CalendarCommon/types';
import { FilterState } from '@/features/events/slice';
import { useTranslation } from 'react-i18next';

export const YearCalendar: React.FC<CalendarControlProps> = ({
  currentCalendarView,
  currentDate,
  activeFilters,
  onNavigate,
}) => {
  const { t } = useTranslation();
  const { events, isLoading, error, handlePrev, handleNext, handleToday, handleViewChange } =
    useCalendarViewData(currentCalendarView, currentDate, activeFilters, onNavigate);

  const handleFilterChangeInHeader = (newFilters: Partial<FilterState>) => {
    onNavigate({ filters: newFilters });
  };

  const handleMonthSelect = (selectedMonthDate: Date) => {
    onNavigate({ view: 'month', date: selectedMonthDate });
  };

  const handleDaySelect = (selectedDayDate: Date) => {
    onNavigate({ view: 'day', date: selectedDayDate });
  };

  if (isLoading && events.length === 0) {
    return <LoadingIndicator />;
  }

  if (error && events.length === 0) {
    return <ErrorMessage defaultMessage={t(error, 'Ошибка загрузки календаря')} />;
  }

  return (
    <Paper
      elevation={0}
      sx={{
        p: { xs: 0, sm: 1 },
        maxWidth: '100%',
        border: '1px solid #eee',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        minHeight: { xs: '70vh', sm: '75vh' },
        position: 'relative',
      }}
    >
      {error && (
        <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, zIndex: 10, p: 1 }}>
          <Paper elevation={2} sx={{ p: 1, bgcolor: 'error.light', color: 'error.contrastText' }}>
            <Typography variant="caption">{t(error, 'Ошибка при обновлении')}</Typography>
          </Paper>
        </Box>
      )}
      <YearCalendarHeader
        currentDate={currentDate}
        currentView={currentCalendarView}
        onPrev={handlePrev}
        onNext={handleNext}
        onToday={handleToday}
        onViewChange={handleViewChange}
        activeFilters={activeFilters}
        onFilterChange={handleFilterChangeInHeader}
      />
      <YearCalendarGrid
        currentDate={currentDate}
        events={events}
        onMonthClick={handleMonthSelect}
        onDayClick={handleDaySelect}
      />
    </Paper>
  );
};
