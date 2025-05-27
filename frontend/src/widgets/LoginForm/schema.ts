import { LoginUserV1AuthLoginPostApiArg } from '@/shared/api/api';
import { z } from '@/shared/config/i18n';

export const LoginSchema = z.object({
  email: z.string().email().trim().min(1),
  password: z.string().trim().min(1),
});

export const mapLoginToRequest = (
  data: z.infer<typeof LoginSchema>,
): LoginUserV1AuthLoginPostApiArg => ({
  authenticateUserModelDto: {
    email: data.email,
    password: data.password,
  },
});

export const mapLoginErrors = {
  401: () => ({
    email: 'Неверный логин или пароль',
    password: 'Неверный логин или пароль',
  }),
};
