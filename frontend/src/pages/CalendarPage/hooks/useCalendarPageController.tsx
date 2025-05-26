import { useCallback, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router';
import { useAppSelector } from '@/shared/store/hooks';
import { selectFilterVariants } from '@/features/events/slice';
import { AppPaths } from '@/shared/routes';
import { CalendarNavOptions } from '@/widgets/CalendarCommon/types';
import { useCalendarUrlParams } from '@/features/events/hooks/useCalendarURLParams';

export const useCalendarPageController = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { currentCalendarView, currentDate, activeFilters, isInitialRedirectNeeded } =
    useCalendarUrlParams();
  const filterVariants = useAppSelector(selectFilterVariants);

  const handleNavigation = useCallback(
    (options: CalendarNavOptions) => {
      const targetView = options.view || currentCalendarView;
      const targetDate = options.date || currentDate;

      const queryUrlParams: Record<string, string | null> = {
        type: activeFilters.type,
        format: activeFilters.format,
        organization: null,
      };

      if (activeFilters.organizationId !== null) {
        const org = filterVariants.organizations.find((o) => o.id === activeFilters.organizationId);
        if (org) queryUrlParams.organization = org.title;
      }

      if (options.filters) {
        if (options.filters.hasOwnProperty('type')) {
          queryUrlParams.type = options.filters.type || null;
        }
        if (options.filters.hasOwnProperty('format')) {
          queryUrlParams.format = options.filters.format || null;
        }
        if (options.filters.hasOwnProperty('organizationId')) {
          const orgId = options.filters.organizationId;
          if (orgId === null) {
            queryUrlParams.organization = null;
          } else {
            const org = filterVariants.organizations.find((o) => o.id === orgId);
            queryUrlParams.organization = org ? org.title : null;
          }
        }
      }

      const newPath = AppPaths.calendar(targetView, targetDate, queryUrlParams);
      navigate(newPath, { replace: true });
    },
    [currentCalendarView, currentDate, activeFilters, filterVariants.organizations, navigate],
  );

  useEffect(() => {
    if (isInitialRedirectNeeded) {
      const currentQueryFromUrl: Record<string, string | null> = {};
      searchParams.forEach((value, key) => {
        currentQueryFromUrl[key] = value;
      });
      const redirectView = currentCalendarView;
      const redirectDate = currentDate;
      const defaultPath = AppPaths.calendar(redirectView, redirectDate, currentQueryFromUrl);
      navigate(defaultPath, { replace: true });
    }
  }, [isInitialRedirectNeeded, currentCalendarView, currentDate, searchParams, navigate]);

  return {
    currentCalendarView,
    currentDate,
    activeFilters,
    handleNavigation,
    isInitialRedirectNeeded,
  };
};
