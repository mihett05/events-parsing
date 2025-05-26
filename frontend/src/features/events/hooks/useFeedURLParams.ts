import { useSearchParams } from 'react-router';
import { useMemo } from 'react';
import { FilterState, selectFilterVariants } from '@/features/events/slice';
import { useAppSelector } from '@/shared/store/hooks';
import { EventFormatEnum, EventTypeEnum } from '@/shared/api/api';

export const useFeedUrlParams = (): { activeFilters: FilterState } => {
  const [searchParams] = useSearchParams();
  const filterVariants = useAppSelector(selectFilterVariants);

  const activeFilters = useMemo((): FilterState => {
    const type = searchParams.get('type') as EventTypeEnum | null;
    const format = searchParams.get('format') as EventFormatEnum | null;
    const organizationName = searchParams.get('organization');

    let organizationId: number | null = null;
    if (organizationName && filterVariants.organizations.length > 0) {
      const foundOrg = filterVariants.organizations.find((org) => org.title === organizationName);
      organizationId = foundOrg ? foundOrg.id : null;
    }
    return {
      type: type || null,
      format: format || null,
      organizationId,
    };
  }, [searchParams, filterVariants.organizations]);

  return { activeFilters };
};
