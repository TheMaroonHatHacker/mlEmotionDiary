"use client";

import { useState, useEffect } from "react";
import { useFormState } from "react-dom";

import { type SignupResult, signup } from "@/actions/signup";
import { SubmitButton } from "@/components/submitButton";

function SignupForm() {
  const [state, signupAction] = useFormState<SignupResult, FormData>(
    signup,
    null,
  );

  return (
    <form action={signupAction} className="form-control">
      <label className="label" htmlFor="username">
        Username
      </label>
      <input
        className="input input-bordered mb-4"
        name="username"
        type="text"
        placeholder="e.g Jon Doe"
        required
      />
      <label className="label" htmlFor="password">
        Password
      </label>
      <input
        className="input input-bordered mb-4"
        name="password"
        type="password"
        required
      />
      <button className="btn" type="submit">
        Submit
      </button>
      {state && !state.success && (
        <div className="alert alert-error">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 shrink-0 stroke-current"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span>{state.message}</span>
        </div>
      )}
    </form>
  );
}

export { SignupForm };