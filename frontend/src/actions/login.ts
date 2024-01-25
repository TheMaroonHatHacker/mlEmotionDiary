"use server";

export async function login(data: FormData) {
  const username = data.get("username");
  const password = data.get("password");

  if (typeof username !== "string" || typeof password !== "string") {
  }

  await fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    body: data,
  });
}