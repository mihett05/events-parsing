import React from 'react';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
} from '@mui/icons-material';
import { format, isValid } from 'date-fns';
import { ru } from 'date-fns/locale';
import { useTranslation } from 'react-i18next';
import { CalendarView } from '@/features/events/slice';
import { CalendarFilters } from '@/features/events/filter/ui/EventsFilter';

interface CalendarHeaderProps {
  currentDate: Date;
  currentView: CalendarView;
  onPrev: () => void;
  onNext: () => void;
  onToday: () => void;
  onViewChange: (newView: CalendarView) => void;
}

export const CalendarHeader: React.FC<CalendarHeaderProps> = ({
  currentDate,
  currentView,
  onPrev,
  onNext,
  onToday,
  onViewChange,
}) => {
  const { t } = useTranslation();

  const formattedDate = isValid(currentDate)
    ? format(currentDate, 'LLLL yyyy', { locale: ru })
    : t('calendar.loading');

  const handleViewChange = (event: SelectChangeEvent<CalendarView>) => {
    const newView = event.target.value as CalendarView;
    onViewChange(newView);
  };

  return (
    <>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        mb={1}
        px={{ xs: 1, sm: 2 }}
        py={1}
        sx={{ borderBottom: '1px solid #eee', flexShrink: 0 }}
      >
        <Stack direction="row" spacing={0.5} alignItems="center">
          <Button
            variant="outlined"
            size="small"
            onClick={onToday}
            sx={{ textTransform: 'none', mr: 0.5 }}
          >
            {t('calendar.today')}
          </Button>
          <IconButton size="small" onClick={onPrev} title={t('calendar.previousMonth')}>
            <ChevronLeftIcon />
          </IconButton>
          <IconButton size="small" onClick={onNext} title={t('calendar.nextMonth')}>
            <ChevronRightIcon />
          </IconButton>
        </Stack>
        <Typography
          variant="h6"
          component="h2"
          sx={{
            fontWeight: 500,
            textAlign: 'center',
            fontSize: { xs: '1.1rem', sm: '1.25rem' },
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            mx: 1,
          }}
        >
          {formattedDate}
        </Typography>
        <FormControl size="small" variant="outlined" sx={{ minWidth: 100, ml: 1 }}>
          <Select
            labelId="calendar-view-select-label"
            id="calendar-view-select"
            value={currentView}
            onChange={handleViewChange}
            sx={{ fontSize: '0.875rem' }}
          >
            <MenuItem value="day">{t('calendar.view.day')}</MenuItem>
            <MenuItem value="month">{t('calendar.view.month')}</MenuItem>
            <MenuItem value="year">{t('calendar.view.year')}</MenuItem>
          </Select>
        </FormControl>
      </Stack>
      <CalendarFilters />
    </>
  );
};
