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
import { isValid, getYear } from 'date-fns';
import { useTranslation } from 'react-i18next';
import { CalendarView as AppCalendarView, FilterState } from '@/features/events/slice';
import { CalendarFilters } from '@/features/events/filter/ui/EventsFilter';
import { InputLabel } from '@mui/material';

interface YearCalendarHeaderProps {
  currentDate: Date;
  currentView: AppCalendarView;
  onPrev: () => void;
  onNext: () => void;
  onToday: () => void;
  onViewChange: (newView: AppCalendarView) => void;
  activeFilters: FilterState;
  onFilterChange: (newFilters: Partial<FilterState>) => void;
}

export const YearCalendarHeader: React.FC<YearCalendarHeaderProps> = React.memo(
  ({
    currentDate,
    currentView,
    onPrev,
    onNext,
    onToday,
    onViewChange,
    activeFilters,
    onFilterChange,
  }) => {
    const { t } = useTranslation();

    const currentYear = isValid(currentDate) ? getYear(currentDate) : '...';
    const formattedTitle = t('yearView.title', { year: currentYear });

    const handleViewSelectChange = (event: SelectChangeEvent<AppCalendarView>) => {
      onViewChange(event.target.value as AppCalendarView);
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
              title={t('calendar.today')}
            >
              {t('calendar.today')}
            </Button>
            <IconButton size="small" onClick={onPrev} title={t('calendar.previousYear')}>
              <ChevronLeftIcon />
            </IconButton>
            <IconButton size="small" onClick={onNext} title={t('calendar.nextYear')}>
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
            {formattedTitle}
          </Typography>
          <FormControl size="small" variant="outlined" sx={{ minWidth: 100, ml: 1 }}>
            <InputLabel id="calendar-view-select-label-year" sx={{ display: 'none' }}>
              {t('calendar.view.view', 'Вид')}
            </InputLabel>
            <Select
              labelId="calendar-view-select-label-year"
              id="calendar-view-select-year"
              value={currentView}
              onChange={handleViewSelectChange}
              sx={{ fontSize: '0.875rem' }}
            >
              <MenuItem value="day">{t('calendar.view.day')}</MenuItem>
              <MenuItem value="month">{t('calendar.view.month')}</MenuItem>
              <MenuItem value="year">{t('calendar.view.year')}</MenuItem>
            </Select>
          </FormControl>
        </Stack>
        <CalendarFilters activeFilters={activeFilters} onFilterChange={onFilterChange} />
      </>
    );
  },
);
