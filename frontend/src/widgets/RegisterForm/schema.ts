import { RegisterUserV1AuthRegisterPostApiArg } from '@/shared/api/api';
import { z } from '@/shared/i18n';

export const RegisterSchema = z.object({
  email: z.string().email().trim().min(1),
  password: z.string().trim().min(1),
  confirmPassword: z.string().trim().min(1),
  fullname: z.string().trim(),
});

export const mapRegisterToRequest = (
  schema: z.infer<typeof RegisterSchema>,
): RegisterUserV1AuthRegisterPostApiArg => ({
  createUserModelDto: {
    email: schema.email,
    password: schema.password,
    fullname: schema.fullname,
  },
});

export const mapRegisterErrors = {
  400: () => ({
    email: 'E-Mail уже занят',
  }),
};
