"use server";

import { FormResult } from "@/types/form";

export type SignupData = {
  username: string;
  jwt: string;
};

export type SignupResult = FormResult<SignupData> | null;

export async function signup(
  prevState: SignupResult,
  data: FormData,
): Promise<SignupResult> {
  const username = data.get("username");
  const password = data.get("password");

  if (typeof username !== "string" || typeof password !== "string") {
  }

  const res = await fetch("http://127.0.0.1:8000/auth/signup", {
    method: "POST",
    body: data,
  });

  return (await res.json()) as SignupResult;
}