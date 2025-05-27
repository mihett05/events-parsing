const KEY = 'accessToken';

export const getToken = (): string | null => {
  return localStorage.getItem(KEY);
};

export const setToken = (token: string) => {
  localStorage.setItem(KEY, token);
};

export const clearToken = () => {
  localStorage.removeItem(KEY);
};
