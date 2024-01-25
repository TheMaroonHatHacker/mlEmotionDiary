"use client";

import * as React from "react";
import { useFormState } from "react-dom";

import { FormAction, FormResult } from "@/types/form";
import { useEffect } from "react";

export type SubmitButtonProps<T> = Omit<
  React.ButtonHTMLAttributes<HTMLButtonElement>,
  "formAction"
> & {
  formAction: FormAction<T>;
};

function SubmitButton<T>({
  formAction: originalFormAction,
  ...props
}: SubmitButtonProps<T>) {
  const [state, formAction] = useFormState<FormResult<T> | null, FormData>(
    originalFormAction,
    null,
  );

  useEffect(() => {
    if (state) {
      if (!state.success) {
        // TODO: Show sign up error toast, probs with DaisyUI to retain styling consistency
        // https://mariojgt.github.io/wind-notify/
        // Seems neat
      }
    }
  });

  return <button className="btn" type="submit" />;
}

export { SubmitButton };