import { useSelector } from 'react-redux';
import {
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Stack,
  Typography,
  SelectChangeEvent,
  CircularProgress,
  Grid,
} from '@mui/material';
import {
  selectFilterVariants,
  selectAreFilterVariantsLoaded,
  FilterState,
  OrganizationFilterOption,
} from '@/features/events/slice';
import {
  EventFormatEnum,
  EventTypeEnum,
  useGetFilterValuesV1EventsFiltersGetQuery,
} from '@/shared/api/api';
import { useTranslation } from 'react-i18next';

const ALL_TYPES_VALUE = 'ALL_TYPES_PLACEHOLDER';
const ALL_FORMATS_VALUE = 'ALL_FORMATS_PLACEHOLDER';
const ALL_ORGANIZATIONS_VALUE = 'ALL_ORGANIZATIONS_PLACEHOLDER';

interface CalendarFiltersProps {
  activeFilters: FilterState;
  onFilterChange: (newFilter: Partial<FilterState>) => void;
}

export const CalendarFilters: React.FC<CalendarFiltersProps> = ({
  activeFilters,
  onFilterChange,
}) => {
  const { t } = useTranslation();
  const filterVariants = useSelector(selectFilterVariants);
  const areVariantsLoaded = useSelector(selectAreFilterVariantsLoaded);

  const { isLoading: isLoadingVariants, isError: isErrorVariants } =
    useGetFilterValuesV1EventsFiltersGetQuery(undefined, {
      skip: areVariantsLoaded,
    });

  const handleInternalFilterChange = (
    filterName: keyof Pick<FilterState, 'type' | 'format' | 'organizationId'>,
    value: string,
  ) => {
    let newFilterPartial: Partial<FilterState> = {};

    if (filterName === 'type') {
      if (value === ALL_TYPES_VALUE) {
        newFilterPartial.type = null;
      } else {
        if (filterVariants.types.includes(value as EventTypeEnum)) {
          newFilterPartial.type = value as EventTypeEnum;
        } else {
          console.warn(`Invalid type value selected: ${value}`);
          newFilterPartial.type = activeFilters.type;
        }
      }
    } else if (filterName === 'format') {
      if (value === ALL_FORMATS_VALUE) {
        newFilterPartial.format = null;
      } else {
        if (filterVariants.formats.includes(value as EventFormatEnum)) {
          newFilterPartial.format = value as EventFormatEnum;
        } else {
          console.warn(`Invalid format value selected: ${value}`);
          newFilterPartial.format = activeFilters.format;
        }
      }
    } else if (filterName === 'organizationId') {
      if (value === ALL_ORGANIZATIONS_VALUE) {
        newFilterPartial.organizationId = null;
      } else {
        const numValue = parseInt(value, 10);
        newFilterPartial.organizationId = isNaN(numValue) ? null : numValue;
      }
    }

    onFilterChange(newFilterPartial);
  };

  if (!areVariantsLoaded && isLoadingVariants) {
    return (
      <Stack
        direction="row"
        spacing={1}
        alignItems="center"
        justifyContent="center"
        sx={{ p: 1, minHeight: 56 }}
      >
        <CircularProgress size={20} />
        <Typography variant="caption">
          {t('calendar.loadingFilters', 'Загрузка фильтров...')}
        </Typography>
      </Stack>
    );
  }

  if (isErrorVariants && !areVariantsLoaded) {
    return (
      <Typography
        color="error"
        variant="caption"
        sx={{ p: 1, minHeight: 56, display: 'flex', alignItems: 'center' }}
      >
        {t('calendar.errorLoadingFilters', 'Ошибка загрузки вариантов фильтров.')}
      </Typography>
    );
  }

  if (
    !areVariantsLoaded ||
    (filterVariants.types.length === 0 &&
      filterVariants.formats.length === 0 &&
      filterVariants.organizations.length === 0)
  ) {
    if (areVariantsLoaded) {
      return (
        <Typography
          variant="caption"
          sx={{ p: 1, minHeight: 56, display: 'flex', alignItems: 'center' }}
        >
          {t('calendar.noAvailableFilters', 'Нет доступных фильтров.')}
        </Typography>
      );
    }
    return null;
  }

  return (
    <Grid container spacing={{ xs: 1, sm: 2 }} sx={{ p: { xs: 1, sm: 1 }, mt: 1, mb: 0.5 }}>
      <Grid size={{ xs: 12, sm: 6, md: 4, lg: 'auto' }}>
        <FormControl size="small" fullWidth margin="dense">
          <InputLabel id="type-filter-label">{t('filter.typeLabel')}</InputLabel>
          <Select
            labelId="type-filter-label"
            id="type-filter-select"
            value={activeFilters.type === null ? ALL_TYPES_VALUE : activeFilters.type}
            label={t('filter.typeLabel')}
            onChange={(event: SelectChangeEvent<string>) =>
              handleInternalFilterChange('type', event.target.value)
            }
          >
            <MenuItem value={ALL_TYPES_VALUE}>{t('filter.allTypes', 'Все типы')}</MenuItem>
            {filterVariants.types.map((typeOption: EventTypeEnum) => (
              <MenuItem key={typeOption} value={typeOption}>
                {typeOption}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 4, lg: 'auto' }}>
        <FormControl size="small" fullWidth margin="dense">
          <InputLabel id="format-filter-label">{t('filter.formatLabel')}</InputLabel>
          <Select
            labelId="format-filter-label"
            id="format-filter-select"
            value={activeFilters.format === null ? ALL_FORMATS_VALUE : activeFilters.format}
            label={t('filter.formatLabel')}
            onChange={(event: SelectChangeEvent<string>) =>
              handleInternalFilterChange('format', event.target.value)
            }
          >
            <MenuItem value={ALL_FORMATS_VALUE}>{t('filter.allFormats', 'Все форматы')}</MenuItem>
            {filterVariants.formats.map((formatOption: EventFormatEnum) => (
              <MenuItem key={formatOption} value={formatOption}>
                {formatOption}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid size={{ xs: 12, sm: 12, md: 4, lg: 'auto' }}>
        <FormControl size="small" fullWidth margin="dense">
          <InputLabel id="organization-filter-label">
            {t('filter.organizationLabel', 'Организация')}
          </InputLabel>
          <Select
            labelId="organization-filter-label"
            id="organization-filter-select"
            value={
              activeFilters.organizationId === null
                ? ALL_ORGANIZATIONS_VALUE
                : activeFilters.organizationId.toString()
            }
            label={t('filter.organizationLabel', 'Организация')}
            onChange={(event: SelectChangeEvent<string>) =>
              handleInternalFilterChange('organizationId', event.target.value)
            }
          >
            <MenuItem value={ALL_ORGANIZATIONS_VALUE}>
              {t('filter.allOrganizations', 'Все организации')}
            </MenuItem>
            {filterVariants.organizations.map((org: OrganizationFilterOption) => (
              <MenuItem key={org.id} value={org.id.toString()}>
                {org.title}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
    </Grid>
  );
};
