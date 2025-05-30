import { Breadcrumbs, Link } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router';
import { Link as RouterLink } from 'react-router';
import { hierarchy, NavigationContext, parseHierarchy } from './hierarchy';

type AdminNavigationProps = {
  context?: NavigationContext;
};

export function AdminNavigation({ context = {} }: AdminNavigationProps) {
  const location = useLocation();
  const { t } = useTranslation('', {
    keyPrefix: 'adminNavigation',
  });

  const parsed = parseHierarchy(location.pathname, context, hierarchy);
  if (!parsed) {
    console.warn('Failed to parse pathname to navigation hierarchy');
    return;
  }

  return (
    <Breadcrumbs>
      {parsed.map((part) => (
        <Link underline="hover" component={RouterLink} to={part.path} color="inherit">
          {t(part.key, {
            ...part.translation(context),
          })}
        </Link>
      ))}
    </Breadcrumbs>
  );
}
