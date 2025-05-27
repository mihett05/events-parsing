import React, { ReactNode } from 'react';
import { useForm, UseFormReturn, FieldValues, SubmitHandler, UseFormProps } from 'react-hook-form';
import { z, ZodType } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Typography } from '@mui/material';

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
  children?: React.ReactNode;
}

export function BaseForm<T extends FieldValues, I, R>({
  config: { form, formMapper, trigger, mutation, errorMappers },
  title,
  children,
}: BaseFormProps<T, I, R>) {
  const onSubmit: SubmitHandler<T> = (data) => {
    trigger(formMapper(data));
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <Typography>{title}</Typography>
      {children}
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
