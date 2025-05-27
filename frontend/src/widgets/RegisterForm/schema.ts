import { RegisterUserV1AuthRegisterPostApiArg } from '@/shared/api/api';
import { z } from '@/shared/config/index';

export const RegisterSchema = z
  .object({
    email: z.string().email().trim().min(1),
    password: z.string().trim().min(1),
    confirmPassword: z.string().min(1),
    firstname: z.string().trim().min(1),
    lastname: z.string().trim().min(1),
    middleName: z.string().trim().optional(),
  })
  .superRefine(({ password, confirmPassword }, ctx) => {
    if (password !== confirmPassword) {
      ctx.addIssue({
        code: 'custom',
        message: 'Пароли не совпадают',
        params: {
          i18n: 'register.invalidConfirmPassword',
        },
        path: ['confirmPassword'],
      });
    }
  });

export const mapRegisterToRequest = (
  schema: z.infer<typeof RegisterSchema>,
): RegisterUserV1AuthRegisterPostApiArg => ({
  createUserModelDto: {
    email: schema.email,
    password: schema.password,
    fullname: [schema.lastname, schema.firstname, schema.middleName]
      .filter((part) => part && part.length > 0)
      .join(' '),
  },
});

export const mapRegisterErrors = {
  400: () => ({
    email: 'E-Mail уже занят',
  }),
};
