import { ErrorMessage } from './ErrorMessage';
import { Loading } from './Loading';

type QueryResult<T> = {
  isLoading: boolean;
  isError: boolean;
  data?: T;
};

type LoaderProps<T> = {
  children: (data: T) => React.ReactNode;
  errorKey?: string;
  query: QueryResult<T>;
};

export function Loader<T>({ children, errorKey, query }: LoaderProps<T>) {
  if (query.isLoading) {
    return <Loading />;
  }

  if (query.isError || !query.data) {
    return <ErrorMessage messageKey={errorKey} />;
  }

  return children(query.data);
}
