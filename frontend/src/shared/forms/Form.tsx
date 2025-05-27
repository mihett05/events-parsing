import React, { ReactNode } from 'react';
import {
  useForm,
  UseFormReturn,
  FieldValues,
  SubmitHandler,
  UseFormProps,
  FormProvider,
} from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Box, Typography } from '@mui/material';

type MutationTrigger<I, R> = (data: I) => {
  unwrap: () => Promise<R>;
};

interface BaseFormConfig<T extends FieldValues, I, R> {
  form: UseFormReturn<T>;
  formMapper: (form: T) => I;
  trigger: MutationTrigger<I, R>;
  mutation: any;
  errorMappers: { [errorCode: number]: (response: R) => { [key in keyof T]?: string } };
}

interface BaseFormProps<T extends FieldValues, I, R> {
  config: BaseFormConfig<T, I, R>;
  title?: string;
  onSuccess?: (response: R) => any;
  children?: React.ReactNode;
}

export function BaseForm<T extends FieldValues, I, R>({
  config: { form, formMapper, trigger, mutation, errorMappers },
  title,
  onSuccess,
  children,
}: BaseFormProps<T, I, R>) {
  const onSubmit: SubmitHandler<T> = async (data) => {
    const response = await trigger(formMapper(data)).unwrap();
    onSuccess?.(response);
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <FormProvider {...form}>
        <Box display="flex" flexDirection="column" gap={2.5}>
          <Typography variant="h6" align="center">
            {title}
          </Typography>
          {children}
        </Box>
      </FormProvider>
    </form>
  );
}

export function useZodForm<
  TFieldValues extends FieldValues = FieldValues,
  TContext = any,
  TTransformedValues = TFieldValues,
>(schema: z.ZodSchema, props: UseFormProps<TFieldValues, TContext, TTransformedValues> = {}) {
  return useForm({
    resolver: zodResolver(schema),
    ...props,
  });
}
