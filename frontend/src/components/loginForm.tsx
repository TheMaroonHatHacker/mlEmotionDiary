"use client";

import { useState, FormEvent, ChangeEvent } from "react";

import { login } from "@/actions/login";

function LoginForm() {
  return (
    <form action={login} className="form-control">
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
      <input className="btn" type="submit" />
    </form>
  );
}

export { LoginForm };