import { UpdateUserV1UsersMePutApiArg } from '@/shared/api/api';
import { z } from '@/shared/config/i18n';

export const UserSchema = z.object({
  firstname: z.string().trim().min(1),
  lastname: z.string().trim().min(1),
  middleName: z.string().trim().optional(),
  sendToType: z.string().refine(
    (value) => {
      return ['EMAIL', 'TELEGRAM'].includes(value);
    },
    {
      params: {
        i18n: 'user.invalidSendToType',
      },
    },
  ),
});

export const mapUserToRequest = (
  data: z.infer<typeof UserSchema>,
): UpdateUserV1UsersMePutApiArg => ({
  updateUserModelDto: {
    fullname: [data.lastname, data.firstname, data.middleName]
      .filter((part) => part && part.length > 0)
      .join(' '),
    sendToType: data.sendToType,
  },
});

export const mapUserErrors = {
  400: () => ({
    sendToType: 'Невалидный способ отправки',
  }),
};
