"use client";
import React, { Dispatch, SetStateAction, useState } from "react";

export const LoginSystem = (props: {setter: Dispatch<SetStateAction<string | null>>}) => {
  
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handleLogin = async () => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    console.log(data["auth"]);
    if (data["auth"] == true) {
      try {
        console.log("username:", username);
        (window as any).localStorage.setItem("username", username);
        props.setter(username);
      } catch (error) {
        console.error("Failed to set item in localStorage:", error);
      }
    } else {
      props.setter("invalid")
    }
  };
  const handleRegister = async () => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const response = await fetch(`http://127.0.0.1:8000/auth/signup`, {
      method: "POST",
      body: formData,
    });
  };

  return (
    <div className="flex flex-col w-96">
      <input
        className="input input-bordered"
        type="text"
        value={username}
        onChange={handleUsernameChange}
        placeholder="Username"
      />
      <input
        className="input input-bordered"
        type="password"
        value={password}
        onChange={handlePasswordChange}
        placeholder="Password"
      />
      <button className="btn" onClick={handleLogin}>
        Login
      </button>
      <button className="btn" onClick={handleRegister}>
        Create
      </button>
    </div>
  );
};

