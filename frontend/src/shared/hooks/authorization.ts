import { useNavigate } from 'react-router';
import { useAppSelector } from '../store/hooks';
import { AppPaths } from '../routes';
import { useEffect } from 'react';

export function useAuthRequired() {
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.user.user);

  useEffect(() => {
    if (user === null) {
      navigate(AppPaths.login());
    }
  }, [user]);

  if (user === null) {
    navigate(AppPaths.login());
    return false;
  }
  return true;
}

export function useAuthProhibited() {
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.user.user);

  useEffect(() => {
    if (user != null) {
      navigate(AppPaths.profile());
    }
  }, [user]);

  if (user != null) {
    navigate(AppPaths.profile());
    return false;
  }

  return true;
}
