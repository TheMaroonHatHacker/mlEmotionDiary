"use server"

export const login = async (username: string, password: string) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    return data;
};