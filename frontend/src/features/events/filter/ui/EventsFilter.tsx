import { useDispatch, useSelector } from 'react-redux';
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
  setFilters,
  selectActiveFilters,
  selectFilterVariants,
  selectAreFilterVariantsLoaded,
  FilterState,
  OrganizationFilterOption,
} from '@/features/events/slice';
import { useGetTypesAndFormatsV1EventsFeedFiltersGetQuery } from '@/shared/api/api';

const ALL_TYPES_VALUE = 'ALL_TYPES_PLACEHOLDER';
const ALL_FORMATS_VALUE = 'ALL_FORMATS_PLACEHOLDER';
const ALL_ORGANIZATIONS_VALUE = 'ALL_ORGANIZATIONS_PLACEHOLDER';

export const CalendarFilters: React.FC = () => {
  const dispatch = useDispatch();
  const activeFilters = useSelector(selectActiveFilters);
  const filterVariants = useSelector(selectFilterVariants);
  const areVariantsLoaded = useSelector(selectAreFilterVariantsLoaded);

  const { isLoading: isLoadingVariants, isError: isErrorVariants } =
    useGetTypesAndFormatsV1EventsFeedFiltersGetQuery(undefined, {
      skip: areVariantsLoaded,
    });

  const handleFilterChange = (
    filterName: keyof Pick<FilterState, 'type' | 'format' | 'organizationId'>,
    value: string | number,
  ) => {
    let actualValue: string | number | null = value;

    if (filterName === 'type') {
      actualValue = value === ALL_TYPES_VALUE ? null : String(value);
    } else if (filterName === 'format') {
      actualValue = value === ALL_FORMATS_VALUE ? null : String(value);
    } else if (filterName === 'organizationId') {
      if (value === ALL_ORGANIZATIONS_VALUE) {
        actualValue = null;
      } else {
        const numValue = parseInt(String(value), 10);
        actualValue = isNaN(numValue) ? null : numValue;
      }
    }
    dispatch(setFilters({ [filterName]: actualValue }));
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
        <Typography variant="caption">Загрузка фильтров...</Typography>
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
        Ошибка загрузки вариантов фильтров.
      </Typography>
    );
  }

  if (
    !areVariantsLoaded &&
    !isLoadingVariants &&
    !isErrorVariants &&
    filterVariants.types.length === 0 &&
    filterVariants.formats.length === 0 &&
    filterVariants.organizations.length === 0
  ) {
    return (
      <Typography
        variant="caption"
        sx={{ p: 1, minHeight: 56, display: 'flex', alignItems: 'center' }}
      >
        Нет доступных фильтров.
      </Typography>
    );
  }

  return (
    <Grid container spacing={{ xs: 1, sm: 2 }} sx={{ p: { xs: 1, sm: 1 }, mt: 1, mb: 0.5 }}>
      <Grid size={{ xs: 12, sm: 4, md: 'auto' }}>
        <FormControl size="small" fullWidth margin="dense">
          <InputLabel id="type-filter-label">Тип события</InputLabel>
          <Select
            labelId="type-filter-label"
            id="type-filter-select"
            value={activeFilters.type === null ? ALL_TYPES_VALUE : activeFilters.type}
            label="Тип события"
            onChange={(event: SelectChangeEvent<string>) =>
              handleFilterChange('type', event.target.value)
            }
          >
            <MenuItem value={ALL_TYPES_VALUE}>Все типы</MenuItem>
            {filterVariants.types.map((typeOption: string) => (
              <MenuItem key={typeOption} value={typeOption}>
                {typeOption}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid size={{ xs: 12, sm: 4, md: 'auto' }}>
        <FormControl size="small" fullWidth margin="dense">
          <InputLabel id="format-filter-label">Формат события</InputLabel>
          <Select
            labelId="format-filter-label"
            id="format-filter-select"
            value={activeFilters.format === null ? ALL_FORMATS_VALUE : activeFilters.format}
            label="Формат события"
            onChange={(event: SelectChangeEvent<string>) =>
              handleFilterChange('format', event.target.value)
            }
          >
            <MenuItem value={ALL_FORMATS_VALUE}>Все форматы</MenuItem>
            {filterVariants.formats.map((formatOption: string) => (
              <MenuItem key={formatOption} value={formatOption}>
                {formatOption}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid size={{ xs: 12, sm: 4, md: 'auto' }}>
        <FormControl size="small" fullWidth margin="dense">
          <InputLabel id="organization-filter-label">Организация</InputLabel>
          <Select
            labelId="organization-filter-label"
            id="organization-filter-select"
            value={
              activeFilters.organizationId === null
                ? ALL_ORGANIZATIONS_VALUE
                : activeFilters.organizationId.toString()
            }
            label="Организация"
            onChange={(event: SelectChangeEvent<string>) =>
              handleFilterChange('organizationId', event.target.value)
            }
          >
            <MenuItem value={ALL_ORGANIZATIONS_VALUE}>Все организации</MenuItem>
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
