import { EventModel, OrganizationModel, UserModel } from '@/shared/api/api';
import { AppPaths } from '@/shared/routes';

type ItemType = 'organizations' | 'organization' | 'users' | 'user' | 'events' | 'event';

export type NavigationContext = {
  organization?: OrganizationModel;
  event?: EventModel;
  user?: UserModel;
};

type KeysOfArray<T extends readonly any[]> = T[number];

type RequiredNavigationContext<TKeys extends readonly (keyof NavigationContext)[] | undefined> =
  TKeys extends readonly (keyof NavigationContext)[]
    ? Required<Pick<NavigationContext, KeysOfArray<TKeys>>>
    : {};

type ItemHierarchyInfo = {
  requiredContext?: readonly (keyof NavigationContext)[];
  translation?: (context: NavigationContext) => Record<string, any>;
  path?: (context: NavigationContext) => string;
  children?: { [key in ItemType]?: ItemHierarchyInfo };
};

function makeHierarchy<TRequired extends readonly (keyof NavigationContext)[] | undefined>(config: {
  requiredContext?: TRequired;
  translation?: (context: RequiredNavigationContext<TRequired>) => Record<string, any>;
  path?: (context: RequiredNavigationContext<TRequired>) => string;
  children?: { [key in ItemType]?: ItemHierarchyInfo };
}): ItemHierarchyInfo {
  return config as ItemHierarchyInfo;
}

export const hierarchy = makeHierarchy({
  children: {
    organizations: makeHierarchy({
      path: () => AppPaths.organizations(),
      children: {
        organization: makeHierarchy({
          requiredContext: ['organization'],
          path: (context) => AppPaths.organization(context.organization.id),
          translation: (context) => ({
            title: context.organization.title,
          }),
          children: {
            events: makeHierarchy({
              requiredContext: ['organization'],
              path: (context) => AppPaths.events(context.organization.id),
              children: {
                event: makeHierarchy({
                  requiredContext: ['organization', 'event'],
                  path: (context) => AppPaths.event(context.event.id),
                  translation: (context) => ({
                    id: context.event.id,
                  }),
                }),
              },
            }),
            users: makeHierarchy({
              requiredContext: ['organization'],
              path: (context) => AppPaths.users(context.organization.id),
              children: {
                user: makeHierarchy({
                  requiredContext: ['organization', 'user'],
                  path: (context) => AppPaths.user(context.organization.id, context.user.id),
                  translation: (context) => ({
                    name: context.user.fullname,
                  }),
                }),
              },
            }),
          },
        }),
      },
    }),
  },
});

type ParsedHierarchy = {
  key: string;
  translation: (context: NavigationContext) => Record<string, any>;
  path: string;
};

export function parseHierarchy(
  pathname: string,
  context: NavigationContext,
  hierarchy: ItemHierarchyInfo,
  key: string | undefined = undefined,
): ParsedHierarchy[] | undefined {
  const part =
    key && hierarchy.path
      ? {
          key,
          translation: hierarchy.translation
            ? hierarchy.translation
            : () => ({}) as Record<string, any>,
          path: hierarchy.path(context),
        }
      : null;

  if (
    part !== null &&
    key &&
    hierarchy.path &&
    validateContext(context, hierarchy.requiredContext || ([] as const)) &&
    hierarchy.path(context) === pathname
  ) {
    return [part];
  }

  if (!hierarchy.children) {
    return;
  }

  for (const childKey of Object.keys(hierarchy.children as object)) {
    const parsed = parseHierarchy(
      pathname,
      context,
      hierarchy.children[childKey as keyof typeof hierarchy.children]!,
      childKey,
    );
    if (parsed) {
      return part ? [part, ...parsed] : parsed;
    }
  }
}

function validateContext(
  providedContext: NavigationContext,
  requiredContext: readonly (keyof NavigationContext)[],
) {
  return requiredContext.every((key) => providedContext[key] !== undefined);
}
