export type FormResult<T> =
  | {
      success: false;
      message: string;
    }
  | {
      success: true;
      data: T;
    };

export type FormAction<T> = (
  prevState: FormResult<T> | null,
  formData: FormData,
) => Promise<FormResult<T>>;