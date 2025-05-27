import {
  BaseQueryFn,
  createApi,
  FetchArgs,
  fetchBaseQuery,
  FetchBaseQueryError,
} from '@reduxjs/toolkit/query/react';
import queryString from 'query-string';
import { clearToken, getToken, setToken } from './tokens';
import { baseApiUrl } from '../config';

const tokenBaseQuery: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
  args,
  api,
  extraOptions,
) => {
  const fetchQuery = fetchBaseQuery({
    baseUrl: baseApiUrl,
    credentials: 'include',
    paramsSerializer: (params) => queryString.stringify(params),
    prepareHeaders: (headers) => {
      if (headers.has('Authorization')) {
        return headers;
      }

      const token = getToken();
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }

      return headers;
    },
  });

  const response = await fetchQuery(args, api, extraOptions);
  const token = getToken();
  if (response.error && token !== null) {
    const refreshResponse = await fetchQuery(
      {
        url: '/v1/auth/refresh',
        method: 'POST',
        cache: 'no-cache',
        credentials: 'include',
      },
      api,
      {},
    );
    if (!refreshResponse.error) {
      const { accessToken } = refreshResponse.data as { accessToken: string };
      setToken(accessToken);
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      if (typeof args === 'string') {
        return fetchQuery(
          {
            url: args,
            headers: {
              ...headers,
            },
          },
          api,
          extraOptions,
        );
      } else {
        return fetchQuery(
          {
            ...args,
            headers: {
              ...args.headers,
              ...headers,
            },
          },
          api,
          extraOptions,
        );
      }
    } else if (refreshResponse.error.status === 401) {
      clearToken();
    }
  }

  return response;
};

export const baseApi = createApi({
  baseQuery: tokenBaseQuery,
  endpoints: () => ({}),
});
