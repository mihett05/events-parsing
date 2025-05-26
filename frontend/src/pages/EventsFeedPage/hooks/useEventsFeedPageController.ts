import { useCallback } from 'react';
import { useNavigate, useLocation } from 'react-router';
import { useAppSelector, useAppDispatch } from '@/shared/store/hooks';
import { FilterState, selectFilterVariants } from '@/features/events/slice';
import { AppPaths } from '@/shared/routes';
import { useFeedUrlParams } from '@/features/events/hooks/useFeedURLParams';

export const useEventsFeedPageController = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const { activeFilters } = useFeedUrlParams();
  const filterVariants = useAppSelector(selectFilterVariants);

  const handleFilterChange = useCallback(
    (newFilters: Partial<FilterState>) => {
      const currentSearchParams = new URLSearchParams(location.search);
      const updatedActiveFiltersState = { ...activeFilters, ...newFilters };

      if (updatedActiveFiltersState.type)
        currentSearchParams.set('type', updatedActiveFiltersState.type);
      else currentSearchParams.delete('type');

      if (updatedActiveFiltersState.format)
        currentSearchParams.set('format', updatedActiveFiltersState.format);
      else currentSearchParams.delete('format');

      if (
        updatedActiveFiltersState.organizationId !== null &&
        updatedActiveFiltersState.organizationId !== undefined
      ) {
        const org = filterVariants.organizations.find(
          (o) => o.id === updatedActiveFiltersState.organizationId,
        );
        if (org) {
          currentSearchParams.set('organization', org.title);
        } else {
          currentSearchParams.delete('organization');
        }
      } else {
        currentSearchParams.delete('organization');
      }

      navigate(`${AppPaths.eventsFeed()}?${currentSearchParams.toString()}`, { replace: true });
    },
    [navigate, location.search, activeFilters, filterVariants.organizations, dispatch],
  );

  return {
    activeFilters,
    handleFilterChange,
  };
};
