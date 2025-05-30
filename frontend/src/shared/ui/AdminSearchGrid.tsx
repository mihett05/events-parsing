import { Box, Paper, TextField, Typography } from '@mui/material';
import Grid from '@mui/material/Grid';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { SerializedError } from '@reduxjs/toolkit';

type AdminSearchGridProps<T> = {
  entities?: T[];
  renderer: (entity: T) => React.ReactNode;
  searchGetter: (entity: T) => string;
  spacing?: number;
  itemSize?: number;
  loadMore?: () => any;
  isLoading?: boolean;
  error?: FetchBaseQueryError | SerializedError;
};

export function AdminSearchGrid<T>({
  entities = [],
  renderer,
  searchGetter,
  loadMore,
  isLoading,
  error,
  spacing = 5,
  itemSize = 3,
}: AdminSearchGridProps<T>) {
  const { t } = useTranslation();
  const [search, setSearch] = useState('');

  const filtered = entities.filter((entity) =>
    searchGetter(entity).trim().toLowerCase().includes(search.trim().toLowerCase()),
  );

  const observer = useRef<IntersectionObserver | null>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !isLoading) {
        loadMore?.();
      }

      if (sentinelRef.current) {
        observer.current?.observe(sentinelRef.current);
      }
    });

    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, [loadMore, isLoading]);

  return (
    <Box display="flex" flexDirection="column" gap={2}>
      <TextField
        label="Поиск"
        variant="outlined"
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
        }}
      />
      <Grid container spacing={spacing}>
        {filtered.map((entity) => (
          <Grid size={itemSize}>{renderer(entity)}</Grid>
        ))}
      </Grid>
      {error && (
        <Paper
          elevation={2}
          sx={{ p: 1, bgcolor: 'error.light', color: 'error.contrastText', mb: 2 }}
        >
          <Typography variant="caption">
            {/*@ts-ignore*/}
            {t(error.messageKey, 'Произошла ошибка при обновлении ленты')}
          </Typography>
        </Paper>
      )}
    </Box>
  );
}

type QueryHook<T> = (
  arg: { page: number; pageSize: number },
  options: {
    refetchOnMountOrArgChange: boolean;
  },
) => {
  isLoading: boolean;
  error?: FetchBaseQueryError | SerializedError;
  data?: T[];
};

export function makeSearchGridHook<T>(hook: QueryHook<T>, pageSize: number = 50) {
  return function innerHook(extra: Record<any, any> = {}) {
    const [page, setPage] = useState(0);
    const { isLoading, data, error } = hook(
      {
        page,
        pageSize,
        ...extra,
      },
      {
        refetchOnMountOrArgChange: true,
      },
    );

    const loadMore = () => setPage((old) => old + 1);

    return {
      isLoading,
      entities: data,
      error,
      loadMore,
    };
  };
}
