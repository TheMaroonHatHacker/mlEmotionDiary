"use client";
import React, { Dispatch, SetStateAction, useState } from "react";

export const LoginSystem = (props: {
  // Defining the function with props for the authentication token, and the setter function
  setter: Dispatch<SetStateAction<string | null>>;
  tokenSetter: Dispatch<SetStateAction<string | null>>;
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handleLogin = async () => {
    const formData = new FormData(); // Creating a new FormData object
    formData.append("username", username); // Appending the username and password to the FormData object
    formData.append("password", password);
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      body: formData,
    }); // Sending a POST request to the server with the FormData object
    const data = await response.json(); // Parsing the response from the server to JSON
    if (data["auth"] == true) {
      try {
        console.log("username:", username);
        (window as any).localStorage.setItem("username", username);
        (window as any).localStorage.setItem("token", data["token"]);
        props.setter(username);
        props.tokenSetter(data["token"]);
      } catch (error) {
        console.error("Failed to set item in localStorage:", error);
      }
    } else {
      props.setter("invalid");
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
